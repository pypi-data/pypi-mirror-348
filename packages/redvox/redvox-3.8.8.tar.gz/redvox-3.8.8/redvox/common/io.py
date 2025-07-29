"""
This module provides IO primitives for working with cross-API RedVox data.
"""
import enum
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from glob import glob
import numpy as np
import json
import os.path
import multiprocessing
import multiprocessing.pool
import tempfile
from pathlib import Path, PurePath
from shutil import copy2, move, rmtree
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Union,
    TYPE_CHECKING,
    Callable,
)

import lz4.frame

from redvox.api900.reader import read_rdvxz_file, read_buffer
from redvox.api900.reader_utils import calculate_uncompressed_size
from redvox.common import api_conversions as ac
from redvox.api1000.common.common import check_type
from redvox.api1000.wrapped_redvox_packet.wrapped_packet import WrappedRedvoxPacketM
from redvox.api1000.proto.redvox_api_m_pb2 import RedvoxPacketM
from redvox.common.versioning import check_version, ApiVersion
from redvox.common.date_time_utils import (
    datetime_from_epoch_microseconds_utc as dt_us,
    datetime_from_epoch_milliseconds_utc as dt_ms,
    datetime_to_epoch_microseconds_utc as us_dt,
    truncate_dt_ymd,
    truncate_dt_ymdh,
)
from redvox.common.parallel_utils import maybe_parallel_map

if TYPE_CHECKING:
    from redvox.api900.wrapped_redvox_packet import WrappedRedvoxPacket
    from redvox.api900.lib.api900_pb2 import RedvoxPacket


def remove_dir_contents(dir_path: Path):
    """
    removes all contents of the directory specified by dir_path

    :param dir_path: path to directory to remove files from
    """
    if dir_path.is_dir():
        for entry in os.listdir(dir_path):
            rmv_path = os.path.join(dir_path, entry)
            if os.path.isdir(rmv_path):
                rmtree(rmv_path)
            else:
                os.remove(rmv_path)
    else:
        print(f"{dir_path} is not a directory; cannot remove contents!")


class FileSystemSaveMode(enum.Enum):
    """
    Enumeration of saving methodology
    """

    MEM = 0  # save using memory
    TEMP = 1  # save using temporary directory
    DISK = 2  # save using path on disk

    @staticmethod
    def get_save_mode(use_temp: bool, use_disk: bool) -> "FileSystemSaveMode":
        """
        :param use_temp: use temporary directory
        :param use_disk: use path on disk
        :return: the mode used to save (use_temp is evaluated before use_disk)
        """
        if use_temp:
            return FileSystemSaveMode.TEMP  # use_temp takes priority
        elif use_disk:
            return FileSystemSaveMode.DISK  # if here, use_temp is always false
        return FileSystemSaveMode.MEM


class FileSystemWriter:
    """
    This class holds basic information about writing and reading objects from a file system
    If user does not enable saving to disk, we use a temporary directory to store large files

    Properties:
        file_name: str, the name of the file (do not include extension)

        file_ext: str, the extension used by the file (do not include the .)  Default "NONE"

        base_dir: str, the directory to save the file to.  Default "." (current dir)

    Protected:
        _save_mode: FileSystemSaveMode, determines how files get saved

        _temp_dir: TemporaryDirectory, temporary directory for large files when not saving to disk
    """

    def __init__(
        self,
        file_name: str,
        file_ext: str = "none",
        base_dir: str = ".",
        save_mode: FileSystemSaveMode = FileSystemSaveMode.MEM,
    ):
        """
        initialize FileSystemWriter

        :param file_name: name of file
        :param file_ext: extension of file, default "none"
        :param base_dir: directory to save file to, default "." (current dir)
        :param save_mode: determines how to save files to system, default MEM (no save, use RAM)
        """
        self.file_name: str = file_name
        self.file_extension: str = file_ext.lower()
        self.base_dir: str = base_dir
        self._save_mode: FileSystemSaveMode = save_mode
        self._temp_dir = tempfile.TemporaryDirectory()

    def __repr__(self):
        return (
            f"file_name: {self.file_name}, "
            f"extension: {self.file_extension}, "
            f"base_dir: {self.base_dir}, "
            f"save_mode: {self._save_mode.value if hasattr(self, '_save_mode') else FileSystemSaveMode.TEMP.value}"
        )

    def __str__(self):
        return (
            f"file_name: {self.file_name}, "
            f"extension: {self.file_extension}, "
            f"base_dir: {self.base_dir}, "
            f"save_mode: {self._save_mode.name if hasattr(self, '_save_mode') else FileSystemSaveMode.TEMP.name}"
        )

    def __del__(self):
        """
        remove temp dir
        """
        self._temp_dir.cleanup()

    def is_use_temp(self) -> bool:
        """
        :return: if writing to temp dir
        """
        if hasattr(self, "_save_mode"):
            return self._save_mode == FileSystemSaveMode.TEMP
        return False

    def set_use_temp(self, use_temp: bool):
        """
        :param use_temp: if true, sets mode to use temp dir, otherwise no change
        """
        if use_temp:
            self._save_mode = FileSystemSaveMode.TEMP

    def get_temp(self) -> str:
        """
        :return: path of temp directory
        """
        return self._temp_dir.name

    def is_use_disk(self) -> bool:
        """
        :return: if writing to path on disk
        """
        if hasattr(self, "_save_mode"):
            return self._save_mode == FileSystemSaveMode.DISK
        return False

    def set_use_disk(self, use_disk: bool):
        """
        :param use_disk: if true, sets mode to use the disk, otherwise no change
        """
        if use_disk:
            self._save_mode = FileSystemSaveMode.DISK

    def is_use_mem(self) -> bool:
        """
        :return: if writing data to memory
        """
        if hasattr(self, "_save_mode"):
            return self._save_mode == FileSystemSaveMode.MEM
        return False

    def set_use_mem(self, use_mem: bool):
        """
        :param use_mem: if true, sets mode to use the system's RAM, otherwise no change
        """
        if use_mem:
            self._save_mode = FileSystemSaveMode.MEM

    def is_save_disk(self) -> bool:
        """
        :return: if writing data to disk (temp dir or user defined path) instead of using memory
        """
        if hasattr(self, "_save_mode"):
            return self._save_mode != FileSystemSaveMode.MEM
        return False

    def save_dir(self) -> str:
        """
        :return: directory where file would be saved based on save mode; returns empty string if saving to memory
        """
        if self.is_use_disk():
            return self.base_dir
        elif self.is_use_temp():
            return self._temp_dir.name
        return ""

    def set_save_mode(self, save_mode: FileSystemSaveMode):
        """
        set the save mode

        :param save_mode: updated save mode
        """
        self._save_mode = save_mode

    def save_mode(self) -> FileSystemSaveMode:
        """
        :return: the save mode
        """
        return self._save_mode.name if hasattr(self, "_save_mode") else FileSystemSaveMode.TEMP

    def full_name(self) -> str:
        """
        :return: file name with extension
        """
        return f"{self.file_name}.{self.file_extension}"

    def full_path(self) -> str:
        """
        :return: the full path to where the file would be written
        """
        return os.path.join(self.save_dir(), self.full_name())

    def set_name_and_extension(self, name: str, ext: str):
        """
        set the name and extension of the output file.  Do not include the . for the extension
        :param name: file name
        :param ext: file extension
        """
        self.file_name = name
        self.file_extension = ext

    def set_name(self, name: str):
        """
        set the name of the output file.
        :param name: file name
        """
        self.file_name = name

    def set_extension(self, ext: str):
        """
        set the extension of the output file.  Do not include the . for the extension
        :param ext: file extension
        """
        self.file_extension = ext

    def json_file_name(self) -> str:
        """
        :return: file name with .json extension
        """
        return f"{self.file_name}.json"

    def json_path(self) -> Path:
        """
        :return: full path to json file
        """
        return Path(self.save_dir()).joinpath(self.json_file_name())

    def create_dir(self):
        """
        if saving to disk, remove the directory if it exists, then create an empty directory to save things into
        if saving to temp dir, remove any files in the temp dir before saving to dir
        """
        if self.is_use_disk():
            if os.path.exists(self.save_dir()):
                remove_dir_contents(Path(self.save_dir()))
            else:
                os.makedirs(self.save_dir())
        elif self.is_use_temp():
            self._temp_dir.cleanup()
            self._temp_dir = tempfile.TemporaryDirectory()

    def as_dict(self) -> dict:
        """
        :return: FileSystemWriter as dictionary
        """
        return {
            "file_name": self.file_name,
            "file_extension": self.file_extension,
            "base_dir": self.base_dir,
            "save_mode": self._save_mode.name if hasattr(self, "_save_mode") else FileSystemSaveMode.TEMP.name,
        }

    @staticmethod
    def from_dict(data_dict: Dict) -> "FileSystemWriter":
        """
        :param data_dict: dictionary to convert to FileSystemWriter
        :return: a FileSystemWriter from dict
        """
        return FileSystemWriter(
            data_dict["file_name"],
            data_dict["file_extension"],
            data_dict["base_dir"],
            FileSystemSaveMode[data_dict["save_mode"]],
        )


def dict_to_json(dct: dict) -> str:
    """
    :param dct: dictionary to convert to json
    :return: dictionary as json string
    """
    return json.dumps(dct)


def json_to_dict(json_str: str) -> Dict:
    """
    :param json_str: string of json to convert to dictionary
    :return: json string as a dictionary
    """
    return json.loads(json_str)


def json_file_to_dict(file_path: str) -> Dict:
    """
    :param file_path: full path of file to load data from.
    :return: json file as python dictionary
    """
    with open(file_path, "r") as f_p:
        return json_to_dict(f_p.read())


def get_json_file(file_dir: str) -> Optional[str]:
    """
    Finds the first json file in the file_dir specified or None if there is no file

    :param file_dir: directory to find json file in
    :return: full name of first json file in the directory or None if no files found
    """
    file_names = glob(os.path.join(file_dir, "*.json"))
    if len(file_names) < 1:
        return None
    return Path(file_names[0]).name


def _is_int(value: str) -> Optional[int]:
    """
    Tests if a given str is a valid integer. If it is, the integer is returned, if it is not, None is returned.

    :param value: The string to test.
    :return: The integer value if it is valid, or None if it is not valid.
    """
    try:
        return int(value)
    except ValueError:
        return None


def _not_none(value: Optional[Any]) -> bool:
    """
    Tests that the given value is not None.

    :param value: The value to test.
    :return: True if the value is not None, False if it is None.
    """
    return value is not None


@dataclass
class IndexEntry:
    """
    This class represents a single index entry. It extracts and encapsulated API agnostic fields that represent the
    information stored in standard RedVox file names.
    """

    full_path: str
    station_id: str
    date_time: datetime
    extension: str
    api_version: ApiVersion
    compressed_file_size_bytes: int = 0
    decompressed_file_size_bytes: int = 0

    @staticmethod
    def from_path(path_str: str, strict: bool = True) -> Optional["IndexEntry"]:
        """
        Attempts to parse a file path into an IndexEntry. If a given path is not recognized as a valid RedVox file,
        None will be returned instead.

        :param path_str: The file system path to attempt to parse.
        :param strict: When set, None is returned if the referenced file DNE.
        :return: Either an IndexEntry or successful parse or None.
        """
        api_version: ApiVersion = check_version(path_str)
        path: Path = Path(path_str)
        name: str = path.stem
        ext: str = path.suffix

        # Attempt to parse file name parts
        split_name = name.split("_")
        if len(split_name) != 2:
            return None

        station_id: str = split_name[0]
        ts_str: str = split_name[1]

        # If you have a filename with a dot, but not an extension, i.e. "0000000001_0.", we need to remove the dot
        # from the end and make in the extension
        if len(ts_str) > 0 and ts_str[-1] == ".":
            ts_str = ts_str[:-1]
            ext = "."

        timestamp: Optional[int] = _is_int(ts_str)

        # Ensure that both the station ID and timestamp can be represented as ints
        if _is_int(station_id) is None or timestamp is None:
            return None

        # Parse the datetime per the specified API version
        date_time: datetime
        if api_version == ApiVersion.API_1000:
            date_time = dt_us(timestamp)
        else:
            date_time = dt_ms(timestamp)

        full_path: str
        try:
            full_path = str(path.resolve(strict=True))
        except FileNotFoundError:
            if strict:
                return None
            full_path = path_str

        return IndexEntry(full_path, station_id, date_time, ext, api_version)._set_compressed_decompressed_lz4_size()

    @staticmethod
    def from_native(entry) -> "IndexEntry":
        """
        Converts a native index entry into a python index entry.

        :param entry: A native index entry.
        :return: A python index entry.
        """
        return IndexEntry(
            entry.full_path,
            entry.station_id,
            dt_us(entry.date_time),
            entry.extension,
            ApiVersion.from_str(entry.api_version),
        )._set_compressed_decompressed_lz4_size()

    def to_native(self):
        import redvox_native

        entry = redvox_native.IndexEntry(
            self.full_path, self.station_id, us_dt(self.date_time), self.extension, self.api_version.value
        )
        return entry

    def _set_compressed_decompressed_lz4_size(self):
        """
        set the compressed and decompressed file size in bytes of a lz4 file being read by the IndexEntry.
        default is 0 for both file sizes

        :return: updated self
        """
        if os.path.exists(self.full_path):
            self.compressed_file_size_bytes = os.path.getsize(self.full_path)
            with open(self.full_path, "rb") as fp:
                if self.api_version == ApiVersion.API_1000:
                    header = lz4.frame.get_frame_info(fp.read())
                    self.decompressed_file_size_bytes = header["content_size"]
                elif self.api_version == ApiVersion.API_900:
                    self.decompressed_file_size_bytes = calculate_uncompressed_size(fp.read())
        return self

    def read(self) -> Optional[Union[WrappedRedvoxPacketM, "WrappedRedvoxPacket"]]:
        """
        Reads, decompresses, deserializes, and wraps the RedVox file pointed to by this entry.

        :return: One of WrappedRedvoxPacket, WrappedRedvoxPacketM, or None.
        """
        if self.api_version == ApiVersion.API_900:
            return read_rdvxz_file(self.full_path)
        elif self.api_version == ApiVersion.API_1000:
            return WrappedRedvoxPacketM.from_compressed_path(self.full_path)
        else:
            return None

    def read_raw(self) -> Optional[Union["RedvoxPacket", RedvoxPacketM]]:
        """
        Reads, decompresses, and deserializes the RedVox file pointed to by this entry.

        :return: One of RedvoxPacket, RedvoxPacketM, or None. Note that these are the raw protobuf types.
        """
        if self.api_version == ApiVersion.API_900:
            with open(self.full_path, "rb") as buf_in:
                return read_buffer(buf_in.read())
        elif self.api_version == ApiVersion.API_1000:
            with lz4.frame.open(self.full_path, "rb") as serialized_in:
                proto: RedvoxPacketM = RedvoxPacketM()
                proto.ParseFromString(serialized_in.read())
                return proto
        else:
            return None

    def _into_native(self):
        pass

    def __eq__(self, other: object) -> bool:
        """
        Tests if this value is equal to another value.
        This along with __lt__ are used to fulfill the total ordering contract. Compares this entry's full path to
        another entries full path.

        :param other: Other IndexEntry to compare against.
        :return: True if this full path is less than the other full path.
        """
        if isinstance(other, IndexEntry):
            return self.full_path == other.full_path

        return False


# noinspection DuplicatedCode
@dataclass
class ReadFilter:
    """
    Filter RedVox files from the file system.
    """

    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    station_ids: Optional[Set[str]] = None
    extensions: Optional[Set[str]] = field(default_factory=lambda: {".rdvxm", ".rdvxz"})
    start_dt_buf: Optional[timedelta] = timedelta(minutes=2.0)
    end_dt_buf: Optional[timedelta] = timedelta(minutes=2.0)
    api_versions: Optional[Set[ApiVersion]] = field(default_factory=lambda: {ApiVersion.API_900, ApiVersion.API_1000})

    @staticmethod
    def empty() -> "ReadFilter":
        """
        :return: A ReadFilter with ALL filters set to None. This is opposed to the default
                 which sets sane defaults for extensions, APIs, and window buffers.
        """
        return ReadFilter(None, None, None, None, None, None, None)

    def clone(self) -> "ReadFilter":
        """
        :return: a copy of the calling ReadFilter
        """
        return_filter = ReadFilter()
        return (
            return_filter.with_start_dt(self.start_dt)
            .with_end_dt(self.end_dt)
            .with_station_ids(self.station_ids)
            .with_extensions(self.extensions)
            .with_start_dt_buf(self.start_dt_buf)
            .with_end_dt_buf(self.end_dt_buf)
            .with_api_versions(self.api_versions)
        )

    def with_start_dt(self, start_dt: Optional[datetime]) -> "ReadFilter":
        """
        Adds a start datetime filter.

        :param start_dt: Start datetime that files should come after.
        :return: A modified instance of this filter
        """
        check_type(start_dt, [datetime, None])
        self.start_dt = start_dt
        return self

    def with_start_ts(self, start_ts: Optional[float]) -> "ReadFilter":
        """
        Adds a start time filter.

        :param start_ts: Start timestamp (microseconds)
        :return: A modified instance of this filter
        """
        check_type(start_ts, [int, float, None])
        if start_ts is None:
            return self.with_start_dt(None)

        return self.with_start_dt(dt_us(start_ts))

    def with_end_dt(self, end_dt: Optional[datetime]) -> "ReadFilter":
        """
        Adds an end datetime filter.

        :param end_dt: Filter for which packets should come before.
        :return: A modified instance of this filter
        """
        check_type(end_dt, [datetime, None])
        self.end_dt = end_dt
        return self

    def with_end_ts(self, end_ts: Optional[float]) -> "ReadFilter":
        """
        Like with_end_dt, but uses a microsecond timestamp.

        :param end_ts: Timestamp microseconds.
        :return: A modified instance of this filter
        """
        check_type(end_ts, [int, float, None])
        if end_ts is None:
            return self.with_end_dt(None)

        return self.with_end_dt(dt_us(end_ts))

    def with_station_ids(self, station_ids: Optional[Set[str]]) -> "ReadFilter":
        """
        Add a station id filter. Filters against provided station ids.

        :param station_ids: Station ids to filter against.
        :return: A modified instance of this filter
        """
        check_type(station_ids, [set, None])
        self.station_ids = station_ids
        return self

    def with_extensions(self, extensions: Optional[Set[str]]) -> "ReadFilter":
        """
        Filters against known file extensions.

        :param extensions: One or more extensions to filter against
        :return: A modified instance of this filter
        """
        check_type(extensions, [set, None])
        self.extensions = extensions
        return self

    def with_start_dt_buf(self, start_dt_buf: Optional[timedelta]) -> "ReadFilter":
        """
        Modifies the time buffer prepended to the start time.

        :param start_dt_buf: Amount of time to buffer before start time.
        :return: A modified instance of self.
        """
        check_type(start_dt_buf, [timedelta, None])
        self.start_dt_buf = start_dt_buf
        return self

    def with_end_dt_buf(self, end_dt_buf: Optional[timedelta]) -> "ReadFilter":
        """
        Modifies the time buffer appended to the end time.

        :param end_dt_buf: Amount of time to buffer after end time.
        :return: A modified instance of self.
        """
        check_type(end_dt_buf, [timedelta, None])
        self.end_dt_buf = end_dt_buf
        return self

    def with_api_versions(self, api_versions: Optional[Set[ApiVersion]]) -> "ReadFilter":
        """
        Filters for specified API versions.

        :param api_versions: A set containing valid ApiVersion enums that should be included.
        :return: A modified instance of self.
        """
        check_type(api_versions, [set, None])
        self.api_versions = api_versions
        return self

    def apply_dt(self, date_time: datetime, dt_fn: Callable[[datetime], datetime] = lambda dt: dt) -> bool:
        """
        Tests if a given datetime passes this filter.

        :param date_time: Datetime to test
        :param dt_fn: An (optional) function that will transform one datetime into another.
        :return: True if the datetime is included, False otherwise
        """
        check_type(date_time, [datetime])
        start_buf: timedelta = timedelta(seconds=0) if self.start_dt_buf is None else self.start_dt_buf
        if self.start_dt is not None and date_time < (dt_fn(self.start_dt - start_buf)):
            return False

        end_buf: timedelta = timedelta(seconds=0) if self.end_dt_buf is None else self.end_dt_buf
        if self.end_dt is not None and date_time > (dt_fn(self.end_dt + end_buf)):
            return False

        return True

    def apply(self, entry: IndexEntry) -> bool:
        """
        Applies this filter to the given IndexEntry.

        :param entry: The entry to test.
        :return: True if the entry is accepted by the filter, False otherwise.
        """
        check_type(entry, [IndexEntry])

        if not self.apply_dt(entry.date_time):
            return False

        if self.station_ids is not None and entry.station_id not in self.station_ids:
            return False

        if self.extensions is not None and entry.extension not in self.extensions:
            return False

        if self.api_versions is not None and entry.api_version not in self.api_versions:
            return False

        return True


@dataclass
class IndexStationSummary:
    """
    Summary of a single station in the index.
    """

    station_id: str
    api_version: ApiVersion
    total_packets: int
    first_packet: datetime
    last_packet: datetime
    single_packet_decompressed_size_bytes: int

    @staticmethod
    def from_entry(entry: IndexEntry) -> "IndexStationSummary":
        """
        Instantiates a new summary from a given IndexEntry.

        :param entry: Entry to copy information from.
        :return: An instance of IndexStationSummary.
        """
        return IndexStationSummary(
            entry.station_id,
            entry.api_version,
            1,
            first_packet=entry.date_time,
            last_packet=entry.date_time,
            single_packet_decompressed_size_bytes=entry.decompressed_file_size_bytes,
        )

    def update(self, entry: IndexEntry) -> None:
        """
        Updates this summary given a new index entry.

        :param entry: Entry to update this summary from.
        """
        self.total_packets += 1
        if entry.date_time < self.first_packet:
            self.first_packet = entry.date_time

        if entry.date_time > self.last_packet:
            self.last_packet = entry.date_time


@dataclass
class IndexSummary:
    """
    Summarizes the contents of the index.
    """

    station_summaries: Dict[ApiVersion, Dict[str, IndexStationSummary]]

    def station_ids(self, api_version: ApiVersion = None) -> List[str]:
        """
        Returns the station IDs referenced by this index.

        :param api_version: An (optional) filter to only return packets for a specified RedVox API version.
                            None will collect station IDs from all API versions.
        :return: The station IDs referenced by this index.
        """
        if api_version is not None:
            return list(
                set(
                    map(
                        lambda summary: summary.station_id,
                        self.station_summaries[api_version].values(),
                    )
                )
            )
        else:
            # noinspection PyTypeChecker
            return list(
                set(
                    map(
                        lambda summary: summary.station_id,
                        self.station_summaries[ApiVersion.API_900].values(),
                    )
                )
            ) + list(
                set(
                    map(
                        lambda summary: summary.station_id,
                        self.station_summaries[ApiVersion.API_1000].values(),
                    )
                )
            )

    def total_packets(self, api_version: ApiVersion = None) -> int:
        """
        Returns the total number of packets referenced by this index.

        :param api_version: An (optional) filter to only return packets for a specified RedVox API version.
                            None will count packets from all API versions.
        :return: The total number of packets referenced by this index.
        """
        if api_version is not None:
            return sum(
                map(
                    lambda summary: summary.total_packets,
                    self.station_summaries[api_version].values(),
                )
            )
        else:
            # noinspection PyTypeChecker
            return sum(
                map(
                    lambda summary: summary.total_packets,
                    self.station_summaries[ApiVersion.API_900].values(),
                )
            ) + sum(
                map(
                    lambda summary: summary.total_packets,
                    self.station_summaries[ApiVersion.API_1000].values(),
                )
            )

    @staticmethod
    def from_index(index: "Index") -> "IndexSummary":
        """
        Builds an IndexSummary from a given index.

        :param index: Index to build summary from.
        :return: An instance of IndexSummary.
        """
        station_summaries: Dict[ApiVersion, Dict[str, IndexStationSummary]] = defaultdict(dict)

        entry: IndexEntry
        for entry in index.entries:
            sub_entry: Dict[str, IndexStationSummary] = station_summaries[entry.api_version]
            if entry.station_id in sub_entry:
                # Update existing station summary
                sub_entry[entry.station_id].update(entry)
            else:
                # Create new station summary
                sub_entry[entry.station_id] = IndexStationSummary.from_entry(entry)

        return IndexSummary(station_summaries)


@dataclass
class Index:
    """
    An index of available RedVox files from the file system.
    """

    entries: List[IndexEntry] = field(default_factory=lambda: [])

    @staticmethod
    def from_native(index_native) -> "Index":
        """
        Converts a native index into a python index.

        :param index_native: A native index.
        :return: A Python index.
        """
        entries: List[IndexEntry] = list(map(IndexEntry.from_native, index_native.entries))
        return Index(entries)._set_decompressed_file_size()

    def to_native(self):
        import redvox_native

        native_index = redvox_native.Index()
        native_index.entries = list(map(IndexEntry.to_native, self.entries))
        return native_index

    def max_decompressed_file_size(self) -> int:
        """
        :return: the maximum decompressed file size in the entries
        """
        return max([fi.decompressed_file_size_bytes for fi in self.entries]) if len(self.entries) > 0 else np.nan

    def get_decompressed_file_size(self) -> int:
        """
        :return: the decompressed size of the first file in the list of entries
        """
        if len(self.entries) == 0:
            return np.nan
        if self.entries[0].decompressed_file_size_bytes == 0 and os.path.exists(self.entries[0].full_path):
            with lz4.frame.open(self.entries[0].full_path, "rb") as fr:
                return len(fr.read())
        return self.entries[0].decompressed_file_size_bytes

    def _set_decompressed_file_size(self) -> "Index":
        """
        updates the decompressed size of all entries if the maximum decompressed size is 0, otherwise makes no changes

        :return: updated self
        """
        if self.max_decompressed_file_size() == 0:
            new_size = self.get_decompressed_file_size()
            for ie in self.entries:
                ie.decompressed_file_size_bytes = new_size
        return self

    def sort(self) -> None:
        """
        Sorts the entries stored in this index.
        """
        self.entries = sorted(
            self.entries,
            key=lambda entry: (entry.api_version, entry.station_id, entry.date_time),
        )

    def append(self, entries: Iterator[IndexEntry]) -> None:
        """
        Appends new entries to this index.

        :param entries: Entries to append.
        """
        self.entries.extend(entries)
        self._set_decompressed_file_size()

    def summarize(self) -> IndexSummary:
        """
        :return: A summary of the contents of this index.
        """
        return IndexSummary.from_index(self)

    def get_index_for_station_id(self, station_id: str) -> "Index":
        """
        :param station_id: id to get entries for
        :return: Index containing only the entries for the station requested
        """
        return Index([en for en in self.entries if en.station_id == station_id])

    def stream_raw(self, read_filter: ReadFilter = ReadFilter()) -> Iterator[Union["RedvoxPacket", RedvoxPacketM]]:
        """
        Read, decompress, deserialize, and then stream RedVox data pointed to by this index.

        :param read_filter: Additional filtering to specify which data should be streamed.
        :return: An iterator over RedvoxPacket and RedvoxPacketM instances.
        """
        filtered: Iterator[IndexEntry] = filter(read_filter.apply, self.entries)
        # noinspection Mypy
        return map(IndexEntry.read_raw, filtered)

    def stream(
        self, read_filter: ReadFilter = ReadFilter()
    ) -> Iterator[Union["WrappedRedvoxPacket", WrappedRedvoxPacketM]]:
        """
        Read, decompress, deserialize, wrap, and then stream RedVox data pointed to by this index.

        :param read_filter: Additional filtering to specify which data should be streamed.
        :return: An iterator over WrappedRedvoxPacket and WrappedRedvoxPacketM instances.
        """
        filtered: Iterator[IndexEntry] = filter(read_filter.apply, self.entries)
        # noinspection Mypy
        return map(IndexEntry.read, filtered)

    def read_raw(self, read_filter: ReadFilter = ReadFilter()) -> List[Union["RedvoxPacket", RedvoxPacketM]]:
        """
        Read, decompress, and deserialize RedVox data pointed to by this index.

        :param read_filter: Additional filtering to specify which data should be read.
        :return: A list of RedvoxPacket and RedvoxPacketM instances.
        """
        return list(self.stream_raw(read_filter))

    def read(self, read_filter: ReadFilter = ReadFilter()) -> List[Union["WrappedRedvoxPacket", WrappedRedvoxPacketM]]:
        """
        Read, decompress, deserialize, and wrap RedVox data pointed to by this index.

        :param read_filter: Additional filtering to specify which data should be read.
        :return: A list of WrappedRedvoxPacket and WrappedRedvoxPacketM instances.
        """
        return list(self.stream(read_filter))

    def files_size(self) -> float:
        """
        :return: sum of file size in bytes of index
        """
        return float(np.sum([entry.decompressed_file_size_bytes for entry in self.entries]))

    def read_contents(self) -> List[RedvoxPacketM]:
        """
        read all the files in the index

        :return: list of RedvoxPacketM, converted from API 900 if necessary
        """
        result: List[RedvoxPacketM] = []

        # Iterate over the API 900 packets in a memory efficient way
        # and convert to API 1000
        # noinspection PyTypeChecker
        for packet_900 in self.stream_raw(ReadFilter.empty().with_api_versions({ApiVersion.API_900})):
            # noinspection Mypy
            result.append(ac.convert_api_900_to_1000_raw(packet_900))

        # Grab the API 1000 packets
        # noinspection PyTypeChecker
        for packet in self.stream_raw(ReadFilter.empty().with_api_versions({ApiVersion.API_1000})):
            # noinspection Mypy
            result.append(packet)

        return result

    def read_first_packet(self) -> Optional[RedvoxPacketM]:
        """
        read the first packet of the index

        :return: single RedvoxPacketM, converted from API 900 if necessary or None if no packet to read
        """
        # Grab the API 1000 packets
        # noinspection PyTypeChecker
        for packet in self.stream_raw(ReadFilter.empty().with_api_versions({ApiVersion.API_1000})):
            # noinspection Mypy
            return packet

        # Iterate over the API 900 packets in a memory efficient way
        # and convert to API 1000
        # noinspection PyTypeChecker
        for packet_900 in self.stream_raw(ReadFilter.empty().with_api_versions({ApiVersion.API_900})):
            # noinspection Mypy
            return ac.convert_api_900_to_1000_raw(packet_900)

        return None


# The following constants are used for identifying valid RedVox API 900 and API 1000 structured directory layouts.
__VALID_YEARS: Set[str] = {f"{i:04}" for i in range(2015, 2031)}
__VALID_MONTHS: Set[str] = {f"{i:02}" for i in range(1, 13)}
__VALID_DATES: Set[str] = {f"{i:02}" for i in range(1, 32)}
__VALID_HOURS: Set[str] = {f"{i:02}" for i in range(0, 24)}


def _list_subdirs(base_dir: str, valid_choices: Set[str]) -> Iterator[str]:
    """
    Lists sub-directors in a given base directory that match the provided choices.

    :param base_dir: Base dir to find sub dirs in.
    :param valid_choices: A list of valid directory names.
    :return: A list of valid subdirs.
    """
    subdirs: Iterator[str] = map(lambda p: PurePath(p).name, glob(os.path.join(base_dir, "*", "")))
    return filter(valid_choices.__contains__, subdirs)


# These fields are set at runtime and provide the implementation (either native or pure python) for IO methods
__INDEX_STRUCTURED_FN: Callable[[str, ReadFilter, Optional[multiprocessing.pool.Pool]], Index]
__INDEX_STRUCTURED_900_FN: Callable[[str, ReadFilter, bool, Optional[multiprocessing.pool.Pool]], Index]
__INDEX_STRUCTURED_1000_FN: Callable[[str, ReadFilter, bool, Optional[multiprocessing.pool.Pool]], Index]
__INDEX_UNSTRUCTURED_FN: Callable[[str, ReadFilter, bool, Optional[multiprocessing.pool.Pool]], Index]


def __map_opt(fn, v):
    """
    Maps the provided function on the value if v is not None, otherwise, returns None.

    :param fn: The mapping function.
    :param v: The optional value to map.
    :return: The optional mapped value.
    """
    if v is None:
        return None
    return fn(v)


def __dur2us(dur: timedelta) -> float:
    """
    Converts a timedelta into microseconds.

    :param dur: timedelta to convert
    :return: Number of microseconds in the time delta.
    """
    return dur.total_seconds() * 1_000_000.0


def __api_native(apis_py: Set[ApiVersion]) -> Set[str]:
    """
    Convert python ApiVersions into native ApiVersions.

    :param apis_py: Python API versions.
    :return: Native API versions.
    """
    r: Set[str] = set()
    for api_py in apis_py:
        if api_py == ApiVersion.API_900:
            r.add("Api900")
            continue
        if api_py == ApiVersion.API_1000:
            r.add("Api1000")

    return r


def index_unstructured_py(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    Returns the list of file paths that match the given filter for unstructured data.

    :param base_dir: Directory containing unstructured data.
    :param read_filter: An (optional) ReadFilter for specifying station IDs and time windows.
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: An iterator of valid paths.
    """
    check_type(base_dir, [str])
    check_type(read_filter, [ReadFilter])

    index: Index = Index()

    extensions: Set[str] = read_filter.extensions if read_filter.extensions is not None else {""}

    all_paths: List[str] = []

    extension: str
    for extension in extensions:
        pattern: str = str(PurePath(base_dir).joinpath(f"*{extension}"))
        paths: List[str] = glob(os.path.join(base_dir, pattern))
        all_paths.extend(paths)

    all_entries: Iterator[Optional[IndexEntry]] = maybe_parallel_map(
        pool,
        IndexEntry.from_path,
        iter(all_paths),
        lambda: len(all_paths) > 128,
        chunk_size=64,
    )

    # if len(all_paths) > 128:
    #     _pool: multiprocessing.pool.Pool = (
    #         multiprocessing.Pool() if pool is None else pool
    #     )
    #     all_entries = _pool.imap(IndexEntry.from_path, iter(all_paths))
    #     if pool is None:
    #         _pool.close()
    # else:
    #     all_entries = map(IndexEntry.from_path, all_paths)

    entries: Iterator[IndexEntry] = filter(read_filter.apply, filter(_not_none, all_entries))

    index.append(entries)

    if sort:
        index.sort()

    return index


def index_structured_api_900_py(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    This parses a structured API 900 directory structure and identifies files that match the provided filter.

    :param base_dir: Base directory (should be named api900)
    :param read_filter: Filter to filter files with
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: A list of wrapped packets on an empty list if none match the filter or none are found
    """
    index: Index = Index()

    _pool: multiprocessing.pool.Pool = multiprocessing.Pool() if pool is None else pool

    for year in _list_subdirs(base_dir, __VALID_YEARS):
        for month in _list_subdirs(os.path.join(base_dir, year), __VALID_MONTHS):
            for day in _list_subdirs(os.path.join(base_dir, year, month), __VALID_DATES):
                # Before scanning for *.rdvxz files, let's see if the current year, month, day, are in the
                # filter's range. If not, we can short circuit and skip getting the *.rdvxz files.
                if not read_filter.apply_dt(datetime(int(year), int(month), int(day)), dt_fn=truncate_dt_ymd):
                    continue

                data_dir: str = os.path.join(base_dir, year, month, day)
                entries: Iterator[IndexEntry] = iter(
                    index_unstructured_py(data_dir, read_filter, sort=False, pool=_pool).entries
                )
                index.append(entries)

    if pool is None:
        _pool.close()

    if sort:
        index.sort()
    return index


def index_structured_api_1000_py(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    This parses a structured API M directory structure and identifies files that match the provided filter.

    :param base_dir: Base directory (should be named api1000)
    :param read_filter: Filter to filter files with
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: A list of wrapped packets on an empty list if none match the filter or none are found
    """
    index: Index = Index()

    _pool: multiprocessing.pool.Pool = multiprocessing.Pool() if pool is None else pool

    for year in _list_subdirs(base_dir, __VALID_YEARS):
        for month in _list_subdirs(os.path.join(base_dir, year), __VALID_MONTHS):
            for day in _list_subdirs(os.path.join(base_dir, year, month), __VALID_DATES):
                for hour in _list_subdirs(os.path.join(base_dir, year, month, day), __VALID_HOURS):
                    # Before scanning for *.rdvxm files, let's see if the current year, month, day, hour are in the
                    # filter's range. If not, we can short circuit and skip getting the *.rdvxm files.
                    if not read_filter.apply_dt(
                        datetime(int(year), int(month), int(day), int(hour)),
                        dt_fn=truncate_dt_ymdh,
                    ):
                        continue

                    data_dir: str = os.path.join(base_dir, year, month, day, hour)
                    entries: Iterator[IndexEntry] = iter(
                        index_unstructured_py(data_dir, read_filter, sort=False, pool=_pool).entries
                    )
                    index.append(entries)

    if pool is None:
        _pool.close()

    if sort:
        index.sort()
    return index


def index_structured_py(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    Indexes both API 900 and API 1000 structured directory layouts.

    :param base_dir: The base_dir may either end with api900, api1000, or be a parent directory to one or both of
                     API 900 and API 1000.
    :param read_filter: Filter to further filter results.
    :param pool: Pool for multiprocessing
    :return: An Index of RedVox files.
    """
    base_path: PurePath = PurePath(base_dir)

    _pool: multiprocessing.pool.Pool = multiprocessing.Pool() if pool is None else pool

    # API 900
    if base_path.name == "api900":
        return index_structured_api_900_py(base_dir, read_filter, pool=_pool)
    # API 1000
    elif base_path.name == "api1000":
        return index_structured_api_1000_py(base_dir, read_filter, pool=_pool)
    # Maybe parent to one or both?
    else:
        index: Index = Index()
        subdirs: List[str] = list(_list_subdirs(base_dir, {"api900", "api1000"}))
        if "api900" in subdirs:
            index.append(
                iter(
                    index_structured_api_900_py(
                        str(base_path.joinpath("api900")),
                        read_filter,
                        sort=False,
                        pool=_pool,
                    ).entries
                )
            )

        if "api1000" in subdirs:
            index.append(
                iter(
                    index_structured_api_1000_py(
                        str(base_path.joinpath("api1000")),
                        read_filter,
                        sort=False,
                        pool=_pool,
                    ).entries
                )
            )

        if pool is None:
            _pool.close()

        index.sort()
        return index


# Here we try to import the redvox_native module which provides natively compiled io functions.
# This dynamically sets which functions are called at runtime. Either the native version (if found)
# or the pure Python version.
try:
    # noinspection PyUnresolvedReferences
    import redvox_native

    def __into_read_filter_native(read_filter: ReadFilter):
        """
        Converts a python read filter into a native read filter.

        :param read_filter: Python read filter to convert.
        :return: A native read filter.
        """
        read_filter_native = redvox_native.ReadFilter()
        read_filter_native.start_dt = __map_opt(us_dt, read_filter.start_dt)
        read_filter_native.end_dt = __map_opt(us_dt, read_filter.end_dt)
        read_filter_native.start_dt_buf = __map_opt(__dur2us, read_filter.start_dt_buf)
        read_filter_native.end_dt_buf = __map_opt(__dur2us, read_filter.end_dt_buf)
        read_filter_native.station_ids = read_filter.station_ids
        read_filter_native.extensions = read_filter.extensions
        read_filter_native.api_versions = __map_opt(__api_native, read_filter.api_versions)

        return read_filter_native

    def __index_structured_900_native(
        base_dir: str,
        read_filter: ReadFilter,
        sort: bool,
        pool: Optional[multiprocessing.pool.Pool],
    ) -> Index:
        """
        This parses a structured API 900 directory structure and identifies files that match the provided filter.

        :param base_dir: Base directory (should be named api900)
        :param read_filter: Filter to filter files with
        :param sort: When True, the resulting Index will be sorted before being returned (default=True).
        :param pool: Pool for multiprocessing (not used in native)
        :return: A list of wrapped packets on an empty list if none match the filter or none are found
        """
        read_filter = __into_read_filter_native(read_filter)
        return Index.from_native(redvox_native.index_structured_900(base_dir, read_filter, sort))

    def __index_structured_1000_native(
        base_dir: str,
        read_filter: ReadFilter,
        sort: bool,
        pool: Optional[multiprocessing.pool.Pool],
    ) -> Index:
        """
        This parses a structured API M directory structure and identifies files that match the provided filter.

        :param base_dir: Base directory (should be named api1000)
        :param read_filter: Filter to filter files with
        :param sort: When True, the resulting Index will be sorted before being returned (default=True).
        :param pool: Pool for multiprocessing (not used in native)
        :return: A list of wrapped packets on an empty list if none match the filter or none are found
        """
        read_filter = __into_read_filter_native(read_filter)
        return Index.from_native(redvox_native.index_structured_1000(base_dir, read_filter, sort))

    def __index_structured_native(
        base_dir: str,
        read_filter: ReadFilter,
        pool: Optional[multiprocessing.pool.Pool],
    ) -> Index:
        """
        Indexes both API 900 and API 1000 structured directory layouts.

        :param base_dir: The base_dir may either end with api900, api1000, or be a parent directory to one or both of
                         API 900 and API 1000.
        :param read_filter: Filter to further filter results.
        :param pool: Pool for multiprocessing (not used in native)
        :return: An Index of RedVox files.
        """
        read_filter = __into_read_filter_native(read_filter)
        return Index.from_native(redvox_native.index_structured(base_dir, read_filter))

    def __index_unstructured_native(
        base_dir: str,
        read_filter: ReadFilter,
        sort: bool,
        pool: Optional[multiprocessing.pool.Pool],
    ) -> Index:
        """
        Returns the list of file paths that match the given filter for unstructured data.

        :param base_dir: Directory containing unstructured data.
        :param read_filter: An (optional) ReadFilter for specifying station IDs and time windows.
        :param sort: When True, the resulting Index will be sorted before being returned (default=True).
        :param pool: Pool for multiprocessing (not used in native implementation)
        :return: An iterator of valid paths.
        """
        read_filter = __into_read_filter_native(read_filter)
        return Index.from_native(redvox_native.index_unstructured(base_dir, read_filter, sort))

    __INDEX_STRUCTURED_FN = __index_structured_native
    __INDEX_STRUCTURED_900_FN = __index_structured_900_native
    __INDEX_STRUCTURED_1000_FN = __index_structured_1000_native
    __INDEX_UNSTRUCTURED_FN = __index_unstructured_native
except ImportError:
    __INDEX_STRUCTURED_900_FN = index_structured_api_900_py
    __INDEX_STRUCTURED_1000_FN = index_structured_api_1000_py
    __INDEX_STRUCTURED_FN = index_structured_py
    __INDEX_UNSTRUCTURED_FN = index_unstructured_py


def index_unstructured(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    Returns the list of file paths that match the given filter for unstructured data.

    :param base_dir: Directory containing unstructured data.
    :param read_filter: An (optional) ReadFilter for specifying station IDs and time windows.
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: An iterator of valid paths.
    """
    return __INDEX_UNSTRUCTURED_FN(base_dir, read_filter, sort, pool)


def index_structured_api_900(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    This parses a structured API 900 directory structure and identifies files that match the provided filter.

    :param base_dir: Base directory (should be named api900)
    :param read_filter: Filter to filter files with
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: A list of wrapped packets on an empty list if none match the filter or none are found
    """
    return __INDEX_STRUCTURED_900_FN(base_dir, read_filter, sort, pool)


def index_structured_api_1000(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    sort: bool = True,
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    This parses a structured API M directory structure and identifies files that match the provided filter.

    :param base_dir: Base directory (should be named api1000)
    :param read_filter: Filter to filter files with
    :param sort: When True, the resulting Index will be sorted before being returned (default=True).
    :param pool: Pool for multiprocessing
    :return: A list of wrapped packets on an empty list if none match the filter or none are found
    """
    return __INDEX_STRUCTURED_1000_FN(base_dir, read_filter, sort, pool)


def index_structured(
    base_dir: str,
    read_filter: ReadFilter = ReadFilter(),
    pool: Optional[multiprocessing.pool.Pool] = None,
) -> Index:
    """
    Indexes both API 900 and API 1000 structured directory layouts.

    :param base_dir: The base_dir may either end with api900, api1000, or be a parent directory to one or both of
                     API 900 and API 1000.
    :param read_filter: Filter to further filter results.
    :param pool: Pool for multiprocessing
    :return: An Index of RedVox files.
    """
    return __INDEX_STRUCTURED_FN(base_dir, read_filter, pool)


def sort_unstructured_redvox_data(
    input_dir: str,
    output_dir: Optional[str] = None,
    read_filter: ReadFilter = ReadFilter(),
    copy: bool = True,
) -> bool:
    """
    takes all redvox files in input_dir and sorts them into appropriate subdirectories

    :param input_dir: directory containing all the files to sort
    :param output_dir: optional directory to put the results in; if this is None, uses the input_dir, default None.
    :param read_filter: optional ReadFilter to limit which files to sort, default empty filter (sort everything)
    :param copy: optional value that when set ensures the file contents are copied into the new structure. When this
                 is set to False, the files will instead be moved.

    :return: True if success, False if failure
    """
    if output_dir is None:
        output_dir = input_dir
    check_type(input_dir, [str])
    check_type(output_dir, [str])
    check_type(read_filter, [ReadFilter])

    if not os.path.exists(input_dir):
        print(f"Directory with files to sort: {input_dir} does not exist.  Stopping program.")
        return False

    if not os.path.exists(output_dir):
        print(f"Base directory for creation: {output_dir} does not exist.  Please create it.  Stopping program.")
        return False

    index: Index = Index()
    extension: str
    for extension in read_filter.extensions:
        pattern: str = str(PurePath(input_dir).joinpath(f"*{extension}"))
        paths: List[str] = glob(os.path.join(input_dir, pattern))
        entries: Iterator[IndexEntry] = filter(read_filter.apply, filter(_not_none, map(IndexEntry.from_path, paths)))
        index.append(entries)

    if len(index.entries) < 1:
        print(f"Directory with files to sort: {input_dir} does not contain Redvox data to read.  Stopping program.")
        return False

    for value in index.entries:
        api_version = value.api_version
        if api_version == ApiVersion.API_1000:
            file_out_dir = str(
                PurePath(output_dir).joinpath(
                    "api1000",
                    f"{value.date_time.year:04}",
                    f"{value.date_time.month:02}",
                    f"{value.date_time.day:02}",
                    f"{value.date_time.hour:02}",
                )
            )
        elif api_version == ApiVersion.API_900:
            file_out_dir = str(
                PurePath(output_dir).joinpath(
                    "api900",
                    f"{value.date_time.year:04}",
                    f"{value.date_time.month:02}",
                    f"{value.date_time.day:02}",
                )
            )
        else:
            print(f"Unknown API version {api_version} found in data.  Stopping program.")
            return False
        os.makedirs(file_out_dir, exist_ok=True)

        if copy:
            copy2(value.full_path, file_out_dir)
        else:
            move(value.full_path, file_out_dir)

    return True

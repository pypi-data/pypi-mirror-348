import collections.abc
import os
from typing import overload

import numpy as np

import symusic.core

class ControlChangeQuarter:
    """
    None
    """

def __init__(self, time: float, number: int, value: int) -> None:
    """
    __init__(self, time: float, number: int, value: int) -> None
    """
    ...

@overload
def __init__(self, other: symusic.core.ControlChangeQuarter) -> None:
    """
    __init__(self, other: symusic.core.ControlChangeQuarter) -> None
    """
    ...

def copy(self, deep: bool = True) -> symusic.core.ControlChangeQuarter: ...
@property
def number(self) -> int: ...
@number.setter
def number(self, arg: int, /) -> None: ...
def shift_time(
    self,
    ofnumpyfset: float,
    inplace: bool = False,
) -> symusic.core.ControlChangeQuarter:
    """
    Shift the event time by offset
    """
    ...

@property
def time(self) -> float: ...
@time.setter
def time(self, arg: float, /) -> None: ...
@property
def ttype(self) -> symusic.core.Quarter: ...
@property
def value(self) -> int: ...
@value.setter
def value(self, arg: int, /) -> None: ...

class ControlChangeQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.ControlChangeQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.ControlChangeQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.ControlChangeQuarterList: ...
    def append(self, arg: symusic.core.ControlChangeQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.ControlChangeQuarterList: ...
    def count(self, arg: symusic.core.ControlChangeQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.ControlChangeQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.ControlChangeQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.ControlChangeQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.ControlChangeQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.ControlChangeQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class ControlChangeSecond:
    """
    None
    """

    def __init__(self, time: float, number: int, value: int) -> None:
        """
        __init__(self, time: float, number: int, value: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.ControlChangeSecond) -> None:
        """
        __init__(self, other: symusic.core.ControlChangeSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.ControlChangeSecond: ...
    @property
    def number(self) -> int: ...
    @number.setter
    def number(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.ControlChangeSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, arg: int, /) -> None: ...

class ControlChangeSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.ControlChangeSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.ControlChangeSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.ControlChangeSecondList: ...
    def append(self, arg: symusic.core.ControlChangeSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.ControlChangeSecondList: ...
    def count(self, arg: symusic.core.ControlChangeSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.ControlChangeSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.ControlChangeSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.ControlChangeSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.ControlChangeSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.ControlChangeSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class ControlChangeTick:
    """
    None
    """

    def __init__(self, time: int, number: int, value: int) -> None:
        """
        __init__(self, time: int, number: int, value: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.ControlChangeTick) -> None:
        """
        __init__(self, other: symusic.core.ControlChangeTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.ControlChangeTick: ...
    @property
    def number(self) -> int: ...
    @number.setter
    def number(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ControlChangeTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, arg: int, /) -> None: ...

class ControlChangeTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.ControlChangeTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.ControlChangeTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.ControlChangeTickList: ...
    def append(self, arg: symusic.core.ControlChangeTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.ControlChangeTickList: ...
    def count(self, arg: symusic.core.ControlChangeTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.ControlChangeTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.ControlChangeTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.ControlChangeTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.ControlChangeTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.ControlChangeTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ControlChangeTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class KeySignatureQuarter:
    """
    None
    """

    def __init__(self, time: float, key: int, tonality: int = 0) -> None:
        """
        __init__(self, time: float, key: int, tonality: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.KeySignatureQuarter) -> None:
        """
        __init__(self, other: symusic.core.KeySignatureQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.KeySignatureQuarter: ...
    @property
    def key(self) -> int: ...
    @key.setter
    def key(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.KeySignatureQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def tonality(self) -> int: ...
    @tonality.setter
    def tonality(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class KeySignatureQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.KeySignatureQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.KeySignatureQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.KeySignatureQuarterList: ...
    def append(self, arg: symusic.core.KeySignatureQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.KeySignatureQuarterList: ...
    def count(self, arg: symusic.core.KeySignatureQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.KeySignatureQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.KeySignatureQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.KeySignatureQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.KeySignatureQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.KeySignatureQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class KeySignatureSecond:
    """
    None
    """

    def __init__(self, time: float, key: int, tonality: int = 0) -> None:
        """
        __init__(self, time: float, key: int, tonality: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.KeySignatureSecond) -> None:
        """
        __init__(self, other: symusic.core.KeySignatureSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.KeySignatureSecond: ...
    @property
    def key(self) -> int: ...
    @key.setter
    def key(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.KeySignatureSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def tonality(self) -> int: ...
    @tonality.setter
    def tonality(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class KeySignatureSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.KeySignatureSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.KeySignatureSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.KeySignatureSecondList: ...
    def append(self, arg: symusic.core.KeySignatureSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.KeySignatureSecondList: ...
    def count(self, arg: symusic.core.KeySignatureSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.KeySignatureSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.KeySignatureSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.KeySignatureSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.KeySignatureSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.KeySignatureSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class KeySignatureTick:
    """
    None
    """

    def __init__(self, time: int, key: int, tonality: int = 0) -> None:
        """
        __init__(self, time: int, key: int, tonality: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.KeySignatureTick) -> None:
        """
        __init__(self, other: symusic.core.KeySignatureTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.KeySignatureTick: ...
    @property
    def key(self) -> int: ...
    @key.setter
    def key(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.KeySignatureTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def tonality(self) -> int: ...
    @tonality.setter
    def tonality(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class KeySignatureTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.KeySignatureTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.KeySignatureTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.KeySignatureTickList: ...
    def append(self, arg: symusic.core.KeySignatureTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.KeySignatureTickList: ...
    def count(self, arg: symusic.core.KeySignatureTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.KeySignatureTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.KeySignatureTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.KeySignatureTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.KeySignatureTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.KeySignatureTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.KeySignatureTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class NoteQuarter:
    """
    None
    """

    def __init__(
        self,
        time: float,
        duration: float,
        pitch: int,
        velocity: int = 0,
    ) -> None:
        """
        __init__(self, time: float, duration: float, pitch: int, velocity: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.NoteQuarter) -> None:
        """
        __init__(self, other: symusic.core.NoteQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.NoteQuarter: ...
    @property
    def duration(self) -> float: ...
    @duration.setter
    def duration(self, arg: float, /) -> None: ...
    def empty(self) -> bool: ...
    @property
    def end(self) -> float: ...
    @end.setter
    def end(self, arg: float, /) -> None: ...
    def ent_time(self) -> float: ...
    @property
    def pitch(self) -> int: ...
    @pitch.setter
    def pitch(self, arg: int, /) -> None: ...
    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.NoteQuarter:
        """
        Shift the pitch by offset
        """
        ...

    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.NoteQuarter:
        """
        Shift the event time by offset
        """
        ...

    def shift_velocity(*args, **kwargs):
        """
        shift_velocity(self, offset: int, inplace: bool = False) -> symusic::Note<symusic::Quarter>

        Shift the velocity by offset
        """
        ...

    @property
    def start(self) -> float: ...
    @start.setter
    def start(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...
    @property
    def velocity(self) -> int: ...
    @velocity.setter
    def velocity(self, arg: int, /) -> None: ...

class NoteQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.NoteQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.NoteQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.NoteQuarterList: ...
    def append(self, arg: symusic.core.NoteQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.NoteQuarterList: ...
    def count(self, arg: symusic.core.NoteQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.NoteQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.NoteQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        arg3: np.typing.NDArray,
        /,
    ) -> symusic.core.NoteQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.NoteQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.NoteQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.NoteQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.NoteQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class NoteSecond:
    """
    None
    """

    def __init__(
        self,
        time: float,
        duration: float,
        pitch: int,
        velocity: int = 0,
    ) -> None:
        """
        __init__(self, time: float, duration: float, pitch: int, velocity: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.NoteSecond) -> None:
        """
        __init__(self, other: symusic.core.NoteSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.NoteSecond: ...
    @property
    def duration(self) -> float: ...
    @duration.setter
    def duration(self, arg: float, /) -> None: ...
    def empty(self) -> bool: ...
    @property
    def end(self) -> float: ...
    @end.setter
    def end(self, arg: float, /) -> None: ...
    def ent_time(self) -> float: ...
    @property
    def pitch(self) -> int: ...
    @pitch.setter
    def pitch(self, arg: int, /) -> None: ...
    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.NoteSecond:
        """
        Shift the pitch by offset
        """
        ...

    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.NoteSecond:
        """
        Shift the event time by offset
        """
        ...

    def shift_velocity(*args, **kwargs):
        """
        shift_velocity(self, offset: int, inplace: bool = False) -> symusic::Note<symusic::Second>

        Shift the velocity by offset
        """
        ...

    @property
    def start(self) -> float: ...
    @start.setter
    def start(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...
    @property
    def velocity(self) -> int: ...
    @velocity.setter
    def velocity(self, arg: int, /) -> None: ...

class NoteSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.NoteSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.NoteSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.NoteSecondList: ...
    def append(self, arg: symusic.core.NoteSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.NoteSecondList: ...
    def count(self, arg: symusic.core.NoteSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.NoteSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.NoteSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        arg3: np.typing.NDArray,
        /,
    ) -> symusic.core.NoteSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.NoteSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.NoteSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.NoteSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.NoteSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class NoteTick:
    """
    None
    """

    def __init__(self, time: int, duration: int, pitch: int, velocity: int = 0) -> None:
        """
        __init__(self, time: int, duration: int, pitch: int, velocity: int = 0) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.NoteTick) -> None:
        """
        __init__(self, other: symusic.core.NoteTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.NoteTick: ...
    @property
    def duration(self) -> int: ...
    @duration.setter
    def duration(self, arg: int, /) -> None: ...
    def empty(self) -> bool: ...
    @property
    def end(self) -> int: ...
    @end.setter
    def end(self, arg: int, /) -> None: ...
    def ent_time(self) -> int: ...
    @property
    def pitch(self) -> int: ...
    @pitch.setter
    def pitch(self, arg: int, /) -> None: ...
    def shift_pitch(self, offset: int, inplace: bool = False) -> symusic.core.NoteTick:
        """
        Shift the pitch by offset
        """
        ...

    def shift_time(self, offset: int, inplace: bool = False) -> symusic.core.NoteTick:
        """
        Shift the event time by offset
        """
        ...

    def shift_velocity(*args, **kwargs):
        """
        shift_velocity(self, offset: int, inplace: bool = False) -> symusic::Note<symusic::Tick>

        Shift the velocity by offset
        """
        ...

    @property
    def start(self) -> int: ...
    @start.setter
    def start(self, arg: int, /) -> None: ...
    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...
    @property
    def velocity(self) -> int: ...
    @velocity.setter
    def velocity(self, arg: int, /) -> None: ...

class NoteTickList:
    """
    None
    """

    def __init__(self, arg: collections.abc.Iterable[symusic.core.NoteTick], /) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.NoteTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.NoteTickList: ...
    def append(self, arg: symusic.core.NoteTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.NoteTickList: ...
    def count(self, arg: symusic.core.NoteTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.NoteTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.NoteTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        arg3: np.typing.NDArray,
        /,
    ) -> symusic.core.NoteTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.NoteTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.NoteTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.NoteTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.NoteTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class PedalQuarter:
    """
    None
    """

    def __init__(self, time: float, duration: float) -> None:
        """
        __init__(self, time: float, duration: float) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PedalQuarter) -> None:
        """
        __init__(self, other: symusic.core.PedalQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PedalQuarter: ...
    @property
    def duration(self) -> float: ...
    @duration.setter
    def duration(self, arg: float, /) -> None: ...
    @property
    def end(self) -> float: ...
    @end.setter
    def end(self, arg: float, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.PedalQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def start(self) -> float: ...
    @start.setter
    def start(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class PedalQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PedalQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PedalQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.PedalQuarterList: ...
    def append(self, arg: symusic.core.PedalQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PedalQuarterList: ...
    def count(self, arg: symusic.core.PedalQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PedalQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PedalQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PedalQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.PedalQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PedalQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PedalQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PedalQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class PedalSecond:
    """
    None
    """

    def __init__(self, time: float, duration: float) -> None:
        """
        __init__(self, time: float, duration: float) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PedalSecond) -> None:
        """
        __init__(self, other: symusic.core.PedalSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PedalSecond: ...
    @property
    def duration(self) -> float: ...
    @duration.setter
    def duration(self, arg: float, /) -> None: ...
    @property
    def end(self) -> float: ...
    @end.setter
    def end(self, arg: float, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.PedalSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def start(self) -> float: ...
    @start.setter
    def start(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class PedalSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PedalSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PedalSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.PedalSecondList: ...
    def append(self, arg: symusic.core.PedalSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PedalSecondList: ...
    def count(self, arg: symusic.core.PedalSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PedalSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PedalSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PedalSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.PedalSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PedalSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PedalSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PedalSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class PedalTick:
    """
    None
    """

    def __init__(self, time: int, duration: int) -> None:
        """
        __init__(self, time: int, duration: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PedalTick) -> None:
        """
        __init__(self, other: symusic.core.PedalTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PedalTick: ...
    @property
    def duration(self) -> int: ...
    @duration.setter
    def duration(self, arg: int, /) -> None: ...
    @property
    def end(self) -> int: ...
    @end.setter
    def end(self, arg: int, /) -> None: ...
    def shift_time(self, offset: int, inplace: bool = False) -> symusic.core.PedalTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def start(self) -> int: ...
    @start.setter
    def start(self, arg: int, /) -> None: ...
    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class PedalTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PedalTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PedalTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.PedalTickList: ...
    def append(self, arg: symusic.core.PedalTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PedalTickList: ...
    def count(self, arg: symusic.core.PedalTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PedalTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PedalTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PedalTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.PedalTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PedalTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PedalTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PedalTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class PitchBendQuarter:
    """
    None
    """

    def __init__(self, time: float, value: int) -> None:
        """
        __init__(self, time: float, value: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PitchBendQuarter) -> None:
        """
        __init__(self, other: symusic.core.PitchBendQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PitchBendQuarter: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.PitchBendQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, arg: int, /) -> None: ...

class PitchBendQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PitchBendQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PitchBendQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.PitchBendQuarterList: ...
    def append(self, arg: symusic.core.PitchBendQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PitchBendQuarterList: ...
    def count(self, arg: symusic.core.PitchBendQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PitchBendQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PitchBendQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PitchBendQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.PitchBendQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PitchBendQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PitchBendQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PitchBendQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class PitchBendSecond:
    """
    None
    """

    def __init__(self, time: float, value: int) -> None:
        """
        __init__(self, time: float, value: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PitchBendSecond) -> None:
        """
        __init__(self, other: symusic.core.PitchBendSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PitchBendSecond: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.PitchBendSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, arg: int, /) -> None: ...

class PitchBendSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PitchBendSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PitchBendSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.PitchBendSecondList: ...
    def append(self, arg: symusic.core.PitchBendSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PitchBendSecondList: ...
    def count(self, arg: symusic.core.PitchBendSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PitchBendSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PitchBendSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PitchBendSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.PitchBendSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PitchBendSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PitchBendSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PitchBendSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class PitchBendTick:
    """
    None
    """

    def __init__(self, time: int, value: int) -> None:
        """
        __init__(self, time: int, value: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.PitchBendTick) -> None:
        """
        __init__(self, other: symusic.core.PitchBendTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.PitchBendTick: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.PitchBendTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, arg: int, /) -> None: ...

class PitchBendTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.PitchBendTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.PitchBendTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.PitchBendTickList: ...
    def append(self, arg: symusic.core.PitchBendTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.PitchBendTickList: ...
    def count(self, arg: symusic.core.PitchBendTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.PitchBendTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.PitchBendTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.PitchBendTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.PitchBendTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.PitchBendTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.PitchBendTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.PitchBendTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class Quarter:
    """
    None
    """

    def __init__(self) -> None: ...
    def is_time_unit(self) -> bool: ...

class ScoreQuarter:
    """
    None
    """

    def __init__(self, path: str | os.PathLike) -> None:
        """
        Load from midi file
        """
        ...

    @overload
    def __init__(self, other: symusic.core.ScoreQuarter) -> None:
        """
        Copy constructor
        """
        ...

    @overload
    def __init__(self, path: str) -> None:
        """
        Load from midi file
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.ScoreQuarter: ...
    def clip(
        self,
        start: float,
        end: float,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.ScoreQuarter: ...
    def copy(self, deep: bool = True) -> symusic.core.ScoreQuarter: ...
    def dump_abc(self, path: str | os.PathLike, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    @overload
    def dump_abc(self, path: str, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    def dump_midi(self, path: str | os.PathLike) -> None:
        """
        Dump to midi file
        """
        ...

    @overload
    def dump_midi(self, path: str) -> None:
        """
        Dump to midi file
        """
        ...

    def dumps_abc(self, warn: bool = False) -> str:
        """
        Dump to abc string
        """
        ...

    def dumps_midi(self) -> bytes:
        """
        Dump to midi in memory(bytes)
        """
        ...

    def empty(self) -> bool: ...
    def end(self) -> float: ...
    def from_abc(abc: str) -> symusic.core.ScoreQuarter:
        """
        Load from abc string
        """
        ...

    def from_file(
        path: str | os.PathLike,
        format: str | None = None,
    ) -> symusic.core.ScoreQuarter:
        """
        from_file(path: str | os.PathLike, format: str | None = None) -> symusic.core.ScoreQuarter
        """
        ...

    @overload
    def from_file(path: str, format: str | None = None) -> symusic.core.ScoreQuarter:
        """
        from_file(path: str, format: str | None = None) -> symusic.core.ScoreQuarter
        """
        ...

    def from_midi(data: bytes) -> symusic.core.ScoreQuarter:
        """
        Load from midi in memory(bytes)
        """
        ...

    @property
    def key_signatures(self) -> symusic.core.KeySignatureQuarterList: ...
    @key_signatures.setter
    def key_signatures(self, arg: symusic.core.KeySignatureQuarterList, /) -> None: ...
    @property
    def markers(self) -> symusic.core.TextMetaQuarterList: ...
    @markers.setter
    def markers(self, arg: symusic.core.TextMetaQuarterList, /) -> None: ...
    def note_num(self) -> int: ...
    def resample(
        self,
        tpq: int,
        min_dur: float | None = None,
    ) -> symusic.core.ScoreTick:
        """
        Resample to another ticks per quarter
        """
        ...

    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreQuarter: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.ScoreQuarter: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreQuarter: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ScoreQuarter: ...
    def start(self) -> float: ...
    @property
    def tempos(self) -> symusic.core.TempoQuarterList: ...
    @tempos.setter
    def tempos(self, arg: symusic.core.TempoQuarterList, /) -> None: ...
    @property
    def ticks_per_quarter(self) -> int: ...
    @ticks_per_quarter.setter
    def ticks_per_quarter(self, arg: int, /) -> None: ...
    @property
    def time_signatures(self) -> symusic.core.TimeSignatureQuarterList: ...
    @time_signatures.setter
    def time_signatures(
        self,
        arg: symusic.core.TimeSignatureQuarterList,
        /,
    ) -> None: ...
    def to(self, ttype: object, min_dur: object | None = None) -> object:
        """
        Convert to another time unit
        """
        ...

    @property
    def tpq(self) -> int: ...
    @tpq.setter
    def tpq(self, arg: int, /) -> None: ...
    @property
    def tracks(self) -> symusic.core.TrackQuarterList: ...
    @tracks.setter
    def tracks(self, arg: symusic.core.TrackQuarterList, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class ScoreSecond:
    """
    None
    """

    def __init__(self, path: str | os.PathLike) -> None:
        """
        Load from midi file
        """
        ...

    @overload
    def __init__(self, other: symusic.core.ScoreSecond) -> None:
        """
        Copy constructor
        """
        ...

    @overload
    def __init__(self, path: str) -> None:
        """
        Load from midi file
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.ScoreSecond: ...
    def clip(
        self,
        start: float,
        end: float,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.ScoreSecond: ...
    def copy(self, deep: bool = True) -> symusic.core.ScoreSecond: ...
    def dump_abc(self, path: str | os.PathLike, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    @overload
    def dump_abc(self, path: str, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    def dump_midi(self, path: str | os.PathLike) -> None:
        """
        Dump to midi file
        """
        ...

    @overload
    def dump_midi(self, path: str) -> None:
        """
        Dump to midi file
        """
        ...

    def dumps_abc(self, warn: bool = False) -> str:
        """
        Dump to abc string
        """
        ...

    def dumps_midi(self) -> bytes:
        """
        Dump to midi in memory(bytes)
        """
        ...

    def empty(self) -> bool: ...
    def end(self) -> float: ...
    def from_abc(abc: str) -> symusic.core.ScoreSecond:
        """
        Load from abc string
        """
        ...

    def from_file(
        path: str | os.PathLike,
        format: str | None = None,
    ) -> symusic.core.ScoreSecond:
        """
        from_file(path: str | os.PathLike, format: str | None = None) -> symusic.core.ScoreSecond
        """
        ...

    @overload
    def from_file(path: str, format: str | None = None) -> symusic.core.ScoreSecond:
        """
        from_file(path: str, format: str | None = None) -> symusic.core.ScoreSecond
        """
        ...

    def from_midi(data: bytes) -> symusic.core.ScoreSecond:
        """
        Load from midi in memory(bytes)
        """
        ...

    @property
    def key_signatures(self) -> symusic.core.KeySignatureSecondList: ...
    @key_signatures.setter
    def key_signatures(self, arg: symusic.core.KeySignatureSecondList, /) -> None: ...
    @property
    def markers(self) -> symusic.core.TextMetaSecondList: ...
    @markers.setter
    def markers(self, arg: symusic.core.TextMetaSecondList, /) -> None: ...
    def note_num(self) -> int: ...
    def resample(
        self,
        tpq: int,
        min_dur: float | None = None,
    ) -> symusic.core.ScoreTick:
        """
        Resample to another ticks per quarter
        """
        ...

    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreSecond: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.ScoreSecond: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreSecond: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ScoreSecond: ...
    def start(self) -> float: ...
    @property
    def tempos(self) -> symusic.core.TempoSecondList: ...
    @tempos.setter
    def tempos(self, arg: symusic.core.TempoSecondList, /) -> None: ...
    @property
    def ticks_per_quarter(self) -> int: ...
    @ticks_per_quarter.setter
    def ticks_per_quarter(self, arg: int, /) -> None: ...
    @property
    def time_signatures(self) -> symusic.core.TimeSignatureSecondList: ...
    @time_signatures.setter
    def time_signatures(self, arg: symusic.core.TimeSignatureSecondList, /) -> None: ...
    def to(self, ttype: object, min_dur: object | None = None) -> object:
        """
        Convert to another time unit
        """
        ...

    @property
    def tpq(self) -> int: ...
    @tpq.setter
    def tpq(self, arg: int, /) -> None: ...
    @property
    def tracks(self) -> symusic.core.TrackSecondList: ...
    @tracks.setter
    def tracks(self, arg: symusic.core.TrackSecondList, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class ScoreTick:
    """
    None
    """

    def __init__(self, path: str | os.PathLike) -> None:
        """
        Load from midi file
        """
        ...

    @overload
    def __init__(self, other: symusic.core.ScoreTick) -> None:
        """
        Copy constructor
        """
        ...

    @overload
    def __init__(self, path: str) -> None:
        """
        Load from midi file
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.ScoreTick: ...
    def clip(
        self,
        start: int,
        end: int,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.ScoreTick: ...
    def copy(self, deep: bool = True) -> symusic.core.ScoreTick: ...
    def dump_abc(self, path: str | os.PathLike, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    @overload
    def dump_abc(self, path: str, warn: bool = False) -> None:
        """
        Dump to abc file
        """
        ...

    def dump_midi(self, path: str | os.PathLike) -> None:
        """
        Dump to midi file
        """
        ...

    @overload
    def dump_midi(self, path: str) -> None:
        """
        Dump to midi file
        """
        ...

    def dumps_abc(self, warn: bool = False) -> str:
        """
        Dump to abc string
        """
        ...

    def dumps_midi(self) -> bytes:
        """
        Dump to midi in memory(bytes)
        """
        ...

    def empty(self) -> bool: ...
    def end(self) -> int: ...
    def from_abc(abc: str) -> symusic.core.ScoreTick:
        """
        Load from abc string
        """
        ...

    def from_file(
        path: str | os.PathLike,
        format: str | None = None,
    ) -> symusic.core.ScoreTick:
        """
        from_file(path: str | os.PathLike, format: str | None = None) -> symusic.core.ScoreTick
        """
        ...

    @overload
    def from_file(path: str, format: str | None = None) -> symusic.core.ScoreTick:
        """
        from_file(path: str, format: str | None = None) -> symusic.core.ScoreTick
        """
        ...

    def from_midi(data: bytes) -> symusic.core.ScoreTick:
        """
        Load from midi in memory(bytes)
        """
        ...

    @property
    def key_signatures(self) -> symusic.core.KeySignatureTickList: ...
    @key_signatures.setter
    def key_signatures(self, arg: symusic.core.KeySignatureTickList, /) -> None: ...
    @property
    def markers(self) -> symusic.core.TextMetaTickList: ...
    @markers.setter
    def markers(self, arg: symusic.core.TextMetaTickList, /) -> None: ...
    def note_num(self) -> int: ...
    def pianoroll(
        self,
        modes: collections.abc.Sequence[str] = ["frame", "onset"],
        pitch_range: tuple[int, int] = (0, 128),
        encode_velocity: bool = False,
    ) -> np.typing.NDArray: ...
    def resample(self, tpq: int, min_dur: int | None = None) -> symusic.core.ScoreTick:
        """
        Resample to another ticks per quarter
        """
        ...

    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreTick: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreTick: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.ScoreTick: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.ScoreTick: ...
    def start(self) -> int: ...
    @property
    def tempos(self) -> symusic.core.TempoTickList: ...
    @tempos.setter
    def tempos(self, arg: symusic.core.TempoTickList, /) -> None: ...
    @property
    def ticks_per_quarter(self) -> int: ...
    @ticks_per_quarter.setter
    def ticks_per_quarter(self, arg: int, /) -> None: ...
    @property
    def time_signatures(self) -> symusic.core.TimeSignatureTickList: ...
    @time_signatures.setter
    def time_signatures(self, arg: symusic.core.TimeSignatureTickList, /) -> None: ...
    def to(self, ttype: object, min_dur: object | None = None) -> object:
        """
        Convert to another time unit
        """
        ...

    @property
    def tpq(self) -> int: ...
    @tpq.setter
    def tpq(self, arg: int, /) -> None: ...
    @property
    def tracks(self) -> symusic.core.TrackTickList: ...
    @tracks.setter
    def tracks(self, arg: symusic.core.TrackTickList, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class Second:
    """
    None
    """

    def __init__(self) -> None: ...
    def is_time_unit(self) -> bool: ...

class Synthesizer:
    """
    None
    """

    def __init__(
        self,
        sf_path: str | os.PathLike,
        sample_rate: int,
        quality: int,
    ) -> None:
        """
        __init__(self, sf_path: str | os.PathLike, sample_rate: int, quality: int) -> None
        """
        ...

    @overload
    def __init__(self, sf_path: str, sample_rate: int, quality: int) -> None:
        """
        __init__(self, sf_path: str, sample_rate: int, quality: int) -> None
        """
        ...

    def render(
        self,
        score: symusic.core.ScoreSecond,
        stereo: bool = True,
    ) -> np.typing.NDArray:
        """
        render(self, score: symusic.core.ScoreSecond, stereo: bool = True) -> np.ndarray[dtype=float32, shape=(*, *), order='F']
        """
        ...

    @overload
    def render(
        self,
        score: symusic.core.ScoreTick,
        stereo: bool = True,
    ) -> np.typing.NDArray:
        """
        render(self, score: symusic.core.ScoreTick, stereo: bool = True) -> np.ndarray[dtype=float32, shape=(*, *), order='F']
        """
        ...

    @overload
    def render(
        self,
        score: symusic.core.ScoreQuarter,
        stereo: bool = True,
    ) -> np.typing.NDArray:
        """
        render(self, score: symusic.core.ScoreQuarter, stereo: bool = True) -> np.ndarray[dtype=float32, shape=(*, *), order='F']
        """
        ...

class TempoQuarter:
    """
    None
    """

    def __init__(
        self,
        time: float,
        qpm: float | None = None,
        mspq: int | None = None,
    ) -> None:
        """
        __init__(self, time: float, qpm: float | None = None, mspq: int | None = None) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TempoQuarter) -> None:
        """
        __init__(self, other: symusic.core.TempoQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TempoQuarter: ...
    @property
    def mspq(self) -> int: ...
    @mspq.setter
    def mspq(self, arg: int, /) -> None: ...
    @property
    def qpm(self) -> float: ...
    @qpm.setter
    def qpm(self, arg: float, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TempoQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def tempo(self) -> float: ...
    @tempo.setter
    def tempo(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TempoQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TempoQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TempoQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TempoQuarterList: ...
    def append(self, arg: symusic.core.TempoQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TempoQuarterList: ...
    def count(self, arg: symusic.core.TempoQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TempoQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TempoQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.TempoQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.TempoQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TempoQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TempoQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TempoQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TempoSecond:
    """
    None
    """

    def __init__(
        self,
        time: float,
        qpm: float | None = None,
        mspq: int | None = None,
    ) -> None:
        """
        __init__(self, time: float, qpm: float | None = None, mspq: int | None = None) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TempoSecond) -> None:
        """
        __init__(self, other: symusic.core.TempoSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TempoSecond: ...
    @property
    def mspq(self) -> int: ...
    @mspq.setter
    def mspq(self, arg: int, /) -> None: ...
    @property
    def qpm(self) -> float: ...
    @qpm.setter
    def qpm(self, arg: float, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TempoSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def tempo(self) -> float: ...
    @tempo.setter
    def tempo(self, arg: float, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TempoSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TempoSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TempoSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TempoSecondList: ...
    def append(self, arg: symusic.core.TempoSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TempoSecondList: ...
    def count(self, arg: symusic.core.TempoSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TempoSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TempoSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.TempoSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.TempoSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TempoSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TempoSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TempoSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TempoTick:
    """
    None
    """

    def __init__(
        self,
        time: int,
        qpm: float | None = None,
        mspq: int | None = None,
    ) -> None:
        """
        __init__(self, time: int, qpm: float | None = None, mspq: int | None = None) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TempoTick) -> None:
        """
        __init__(self, other: symusic.core.TempoTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TempoTick: ...
    @property
    def mspq(self) -> int: ...
    @mspq.setter
    def mspq(self, arg: int, /) -> None: ...
    @property
    def qpm(self) -> float: ...
    @qpm.setter
    def qpm(self, arg: float, /) -> None: ...
    def shift_time(self, offset: int, inplace: bool = False) -> symusic.core.TempoTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def tempo(self) -> float: ...
    @tempo.setter
    def tempo(self, arg: float, /) -> None: ...
    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TempoTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TempoTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TempoTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.TempoTickList: ...
    def append(self, arg: symusic.core.TempoTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TempoTickList: ...
    def count(self, arg: symusic.core.TempoTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TempoTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TempoTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        /,
    ) -> symusic.core.TempoTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.TempoTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TempoTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TempoTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TempoTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TextMetaQuarter:
    """
    None
    """

    def __init__(self, time: float, text: str) -> None:
        """
        __init__(self, time: float, text: str) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TextMetaQuarter) -> None:
        """
        __init__(self, other: symusic.core.TextMetaQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TextMetaQuarter: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TextMetaQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, arg: str, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TextMetaQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TextMetaQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TextMetaQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TextMetaQuarterList: ...
    def append(self, arg: symusic.core.TextMetaQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TextMetaQuarterList: ...
    def count(self, arg: symusic.core.TextMetaQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TextMetaQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TextMetaQuarterList: ...
    def from_np() -> None: ...
    def insert(self, arg0: int, arg1: symusic.core.TextMetaQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> None: ...
    def pop(self, index: int = -1) -> symusic.core.TextMetaQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TextMetaQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TextMetaQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TextMetaSecond:
    """
    None
    """

    def __init__(self, time: float, text: str) -> None:
        """
        __init__(self, time: float, text: str) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TextMetaSecond) -> None:
        """
        __init__(self, other: symusic.core.TextMetaSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TextMetaSecond: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TextMetaSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, arg: str, /) -> None: ...
    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TextMetaSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TextMetaSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TextMetaSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TextMetaSecondList: ...
    def append(self, arg: symusic.core.TextMetaSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TextMetaSecondList: ...
    def count(self, arg: symusic.core.TextMetaSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TextMetaSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TextMetaSecondList: ...
    def from_np() -> None: ...
    def insert(self, arg0: int, arg1: symusic.core.TextMetaSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> None: ...
    def pop(self, index: int = -1) -> symusic.core.TextMetaSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TextMetaSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TextMetaSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TextMetaTick:
    """
    None
    """

    def __init__(self, time: int, text: str) -> None:
        """
        __init__(self, time: int, text: str) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TextMetaTick) -> None:
        """
        __init__(self, other: symusic.core.TextMetaTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TextMetaTick: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TextMetaTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, arg: str, /) -> None: ...
    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TextMetaTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TextMetaTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TextMetaTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.TextMetaTickList: ...
    def append(self, arg: symusic.core.TextMetaTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TextMetaTickList: ...
    def count(self, arg: symusic.core.TextMetaTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TextMetaTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TextMetaTickList: ...
    def from_np() -> None: ...
    def insert(self, arg0: int, arg1: symusic.core.TextMetaTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> None: ...
    def pop(self, index: int = -1) -> symusic.core.TextMetaTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TextMetaTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TextMetaTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class Tick:
    """
    None
    """

    def __init__(self) -> None: ...
    def is_time_unit(self) -> bool: ...

class TimeSignatureQuarter:
    """
    None
    """

    def __init__(self, time: float, numerator: int, denominator: int) -> None:
        """
        __init__(self, time: float, numerator: int, denominator: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TimeSignatureQuarter) -> None:
        """
        __init__(self, other: symusic.core.TimeSignatureQuarter) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TimeSignatureQuarter: ...
    @property
    def denominator(self) -> int: ...
    @denominator.setter
    def denominator(self, arg: int, /) -> None: ...
    @property
    def numerator(self) -> int: ...
    @numerator.setter
    def numerator(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureQuarter:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TimeSignatureQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TimeSignatureQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TimeSignatureQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureQuarterList: ...
    def append(self, arg: symusic.core.TimeSignatureQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TimeSignatureQuarterList: ...
    def count(self, arg: symusic.core.TimeSignatureQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TimeSignatureQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureQuarterList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.TimeSignatureQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.TimeSignatureQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TimeSignatureQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TimeSignatureQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TimeSignatureSecond:
    """
    None
    """

    def __init__(self, time: float, numerator: int, denominator: int) -> None:
        """
        __init__(self, time: float, numerator: int, denominator: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TimeSignatureSecond) -> None:
        """
        __init__(self, other: symusic.core.TimeSignatureSecond) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TimeSignatureSecond: ...
    @property
    def denominator(self) -> int: ...
    @denominator.setter
    def denominator(self, arg: int, /) -> None: ...
    @property
    def numerator(self) -> int: ...
    @numerator.setter
    def numerator(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureSecond:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> float: ...
    @time.setter
    def time(self, arg: float, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TimeSignatureSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TimeSignatureSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TimeSignatureSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureSecondList: ...
    def append(self, arg: symusic.core.TimeSignatureSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TimeSignatureSecondList: ...
    def count(self, arg: symusic.core.TimeSignatureSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TimeSignatureSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureSecondList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.TimeSignatureSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.TimeSignatureSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TimeSignatureSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TimeSignatureSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TimeSignatureTick:
    """
    None
    """

    def __init__(self, time: int, numerator: int, denominator: int) -> None:
        """
        __init__(self, time: int, numerator: int, denominator: int) -> None
        """
        ...

    @overload
    def __init__(self, other: symusic.core.TimeSignatureTick) -> None:
        """
        __init__(self, other: symusic.core.TimeSignatureTick) -> None
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TimeSignatureTick: ...
    @property
    def denominator(self) -> int: ...
    @denominator.setter
    def denominator(self, arg: int, /) -> None: ...
    @property
    def numerator(self) -> int: ...
    @numerator.setter
    def numerator(self, arg: int, /) -> None: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureTick:
        """
        Shift the event time by offset
        """
        ...

    @property
    def time(self) -> int: ...
    @time.setter
    def time(self, arg: int, /) -> None: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TimeSignatureTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TimeSignatureTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TimeSignatureTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.TimeSignatureTickList: ...
    def append(self, arg: symusic.core.TimeSignatureTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self) -> symusic.core.TimeSignatureTickList: ...
    def count(self, arg: symusic.core.TimeSignatureTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TimeSignatureTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object | None = None,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureTickList: ...
    def from_np(
        arg0: np.typing.NDArray,
        arg1: np.typing.NDArray,
        arg2: np.typing.NDArray,
        /,
    ) -> symusic.core.TimeSignatureTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.TimeSignatureTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def np(self) -> dict: ...
    def pop(self, index: int = -1) -> symusic.core.TimeSignatureTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TimeSignatureTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TimeSignatureTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TrackQuarter:
    """
    None
    """

    def __init__(self) -> None:
        """
        __init__(self, name: str, program: int = 0, is_drum: bool = False) -> None
        __init__(self, other: symusic.core.TrackQuarter) -> None

        Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TrackQuarter: ...
    def clip(
        self,
        start: float,
        end: float,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.TrackQuarter: ...
    @property
    def controls(self) -> symusic.core.ControlChangeQuarterList: ...
    @controls.setter
    def controls(self, arg: symusic.core.ControlChangeQuarterList, /) -> None: ...
    def copy(self, deep: bool = True) -> symusic.core.TrackQuarter: ...
    def empty(self) -> bool: ...
    def end(self) -> float: ...
    @property
    def is_drum(self) -> bool: ...
    @is_drum.setter
    def is_drum(self, arg: bool, /) -> None: ...
    @property
    def lyrics(self) -> symusic.core.TextMetaQuarterList: ...
    @lyrics.setter
    def lyrics(self, arg: symusic.core.TextMetaQuarterList, /) -> None: ...
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, arg: str, /) -> None: ...
    def note_num(self) -> int: ...
    @property
    def notes(self) -> symusic.core.NoteQuarterList: ...
    @notes.setter
    def notes(self, arg: symusic.core.NoteQuarterList, /) -> None: ...
    @property
    def pedals(self) -> symusic.core.PedalQuarterList: ...
    @pedals.setter
    def pedals(self, arg: symusic.core.PedalQuarterList, /) -> None: ...
    @property
    def pitch_bends(self) -> symusic.core.PitchBendQuarterList: ...
    @pitch_bends.setter
    def pitch_bends(self, arg: symusic.core.PitchBendQuarterList, /) -> None: ...
    @property
    def program(self) -> int: ...
    @program.setter
    def program(self, arg: int, /) -> None: ...
    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackQuarter: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TrackQuarter: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackQuarter: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackQuarter: ...
    def start(self) -> float: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TrackQuarterList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TrackQuarter],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TrackQuarterList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TrackQuarterList: ...
    def append(self, arg: symusic.core.TrackQuarter, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TrackQuarterList: ...
    def count(self, arg: symusic.core.TrackQuarter, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TrackQuarterList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object,
        inplace: bool = True,
    ) -> symusic.core.TrackQuarterList: ...
    def insert(self, arg0: int, arg1: symusic.core.TrackQuarter, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def pop(self, index: int = -1) -> symusic.core.TrackQuarter:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TrackQuarter, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackQuarterList: ...
    @property
    def ttype(self) -> symusic.core.Quarter: ...

class TrackSecond:
    """
    None
    """

    def __init__(self) -> None:
        """
        __init__(self, name: str, program: int = 0, is_drum: bool = False) -> None
        __init__(self, other: symusic.core.TrackSecond) -> None

        Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TrackSecond: ...
    def clip(
        self,
        start: float,
        end: float,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.TrackSecond: ...
    @property
    def controls(self) -> symusic.core.ControlChangeSecondList: ...
    @controls.setter
    def controls(self, arg: symusic.core.ControlChangeSecondList, /) -> None: ...
    def copy(self, deep: bool = True) -> symusic.core.TrackSecond: ...
    def empty(self) -> bool: ...
    def end(self) -> float: ...
    @property
    def is_drum(self) -> bool: ...
    @is_drum.setter
    def is_drum(self, arg: bool, /) -> None: ...
    @property
    def lyrics(self) -> symusic.core.TextMetaSecondList: ...
    @lyrics.setter
    def lyrics(self, arg: symusic.core.TextMetaSecondList, /) -> None: ...
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, arg: str, /) -> None: ...
    def note_num(self) -> int: ...
    @property
    def notes(self) -> symusic.core.NoteSecondList: ...
    @notes.setter
    def notes(self, arg: symusic.core.NoteSecondList, /) -> None: ...
    @property
    def pedals(self) -> symusic.core.PedalSecondList: ...
    @pedals.setter
    def pedals(self, arg: symusic.core.PedalSecondList, /) -> None: ...
    @property
    def pitch_bends(self) -> symusic.core.PitchBendSecondList: ...
    @pitch_bends.setter
    def pitch_bends(self, arg: symusic.core.PitchBendSecondList, /) -> None: ...
    @property
    def program(self) -> int: ...
    @program.setter
    def program(self, arg: int, /) -> None: ...
    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackSecond: ...
    def shift_time(
        self,
        offset: float,
        inplace: bool = False,
    ) -> symusic.core.TrackSecond: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackSecond: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackSecond: ...
    def start(self) -> float: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TrackSecondList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TrackSecond],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TrackSecondList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[float],
        new_times: collections.abc.Sequence[float],
        inplace: bool = False,
    ) -> symusic.core.TrackSecondList: ...
    def append(self, arg: symusic.core.TrackSecond, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TrackSecondList: ...
    def count(self, arg: symusic.core.TrackSecond, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TrackSecondList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object,
        inplace: bool = True,
    ) -> symusic.core.TrackSecondList: ...
    def insert(self, arg0: int, arg1: symusic.core.TrackSecond, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def pop(self, index: int = -1) -> symusic.core.TrackSecond:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TrackSecond, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackSecondList: ...
    @property
    def ttype(self) -> symusic.core.Second: ...

class TrackTick:
    """
    None
    """

    def __init__(self) -> None:
        """
        __init__(self, name: str, program: int = 0, is_drum: bool = False) -> None
        __init__(self, other: symusic.core.TrackTick) -> None

        Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.TrackTick: ...
    def clip(
        self,
        start: int,
        end: int,
        clip_end: bool = False,
        inplace: bool = False,
    ) -> symusic.core.TrackTick: ...
    @property
    def controls(self) -> symusic.core.ControlChangeTickList: ...
    @controls.setter
    def controls(self, arg: symusic.core.ControlChangeTickList, /) -> None: ...
    def copy(self, deep: bool = True) -> symusic.core.TrackTick: ...
    def empty(self) -> bool: ...
    def end(self) -> int: ...
    @property
    def is_drum(self) -> bool: ...
    @is_drum.setter
    def is_drum(self, arg: bool, /) -> None: ...
    @property
    def lyrics(self) -> symusic.core.TextMetaTickList: ...
    @lyrics.setter
    def lyrics(self, arg: symusic.core.TextMetaTickList, /) -> None: ...
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, arg: str, /) -> None: ...
    def note_num(self) -> int: ...
    @property
    def notes(self) -> symusic.core.NoteTickList: ...
    @notes.setter
    def notes(self, arg: symusic.core.NoteTickList, /) -> None: ...
    @property
    def pedals(self) -> symusic.core.PedalTickList: ...
    @pedals.setter
    def pedals(self, arg: symusic.core.PedalTickList, /) -> None: ...
    def pianoroll(
        self,
        modes: collections.abc.Sequence[str] = ["frame", "onset"],
        pitch_range: tuple[int, int] = (0, 128),
        encode_velocity: bool = False,
    ) -> np.typing.NDArray: ...
    @property
    def pitch_bends(self) -> symusic.core.PitchBendTickList: ...
    @pitch_bends.setter
    def pitch_bends(self, arg: symusic.core.PitchBendTickList, /) -> None: ...
    @property
    def program(self) -> int: ...
    @program.setter
    def program(self, arg: int, /) -> None: ...
    def shift_pitch(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackTick: ...
    def shift_time(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackTick: ...
    def shift_velocity(
        self,
        offset: int,
        inplace: bool = False,
    ) -> symusic.core.TrackTick: ...
    def sort(
        self,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackTick: ...
    def start(self) -> int: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

class TrackTickList:
    """
    None
    """

    def __init__(
        self,
        arg: collections.abc.Iterable[symusic.core.TrackTick],
        /,
    ) -> None:
        """
        Construct from an iterable object
        """
        ...

    @overload
    def __init__(self, arg: symusic.core.TrackTickList) -> None:
        """
        Shallow Copy constructor
        """
        ...

    def adjust_time(
        self,
        original_times: collections.abc.Sequence[int],
        new_times: collections.abc.Sequence[int],
        inplace: bool = False,
    ) -> symusic.core.TrackTickList: ...
    def append(self, arg: symusic.core.TrackTick, /) -> None:
        """
        Append `arg` to the end of the list.
        """
        ...

    def clear(self) -> None:
        """
        Remove all items from list.
        """
        ...

    def copy(self, deep: bool = True) -> symusic.core.TrackTickList: ...
    def count(self, arg: symusic.core.TrackTick, /) -> int:
        """
        Return number of occurrences of `arg`.
        """
        ...

    def extend(self, arg: symusic.core.TrackTickList, /) -> None:
        """
        Extend `self` by appending elements from `arg`.
        """
        ...

    def filter(
        self,
        function: object,
        inplace: bool = True,
    ) -> symusic.core.TrackTickList: ...
    def insert(self, arg0: int, arg1: symusic.core.TrackTick, /) -> None:
        """
        Insert object `arg1` before index `arg0`.
        """
        ...

    def is_sorted(self, key: object | None = None, reverse: bool = False) -> bool: ...
    def pop(self, index: int = -1) -> symusic.core.TrackTick:
        """
        Remove and return item at `index` (default last).
        """
        ...

    def remove(self, arg: symusic.core.TrackTick, /) -> None:
        """
        Remove first occurrence of `arg`.
        """
        ...

    def sort(
        self,
        key: object | None = None,
        reverse: bool = False,
        inplace: bool = True,
    ) -> symusic.core.TrackTickList: ...
    @property
    def ttype(self) -> symusic.core.Tick: ...

def dump_wav(
    path: str,
    data: np.typing.NDArray,
    sample_rate: int,
    use_int16: bool = True,
) -> None: ...

from __future__ import annotations

import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

from . import core  # type: ignore
from . import types as smt
from .soundfont import BuiltInSF3

if TYPE_CHECKING:
    from numpy import ndarray

__all__ = [
    "TimeUnit",
    "Note",
    "KeySignature",
    "TimeSignature",
    "ControlChange",
    "Tempo",
    "Pedal",
    "PitchBend",
    "TextMeta",
    "Track",
    "Score",
    "Synthesizer",
]

_HERE = Path(__file__).parent
_BIN = _HERE / "bin"
# for win
if os.name == "nt":
    _MIDI2ABC = _BIN / "midi2abc.exe"
    _ABC2MIDI = _BIN / "abc2midi.exe"
# for linux
else:
    _MIDI2ABC = _BIN / "midi2abc"
    _ABC2MIDI = _BIN / "abc2midi"

if not _MIDI2ABC.exists():
    msg_ = f"{_MIDI2ABC} does not exist"
    raise FileNotFoundError(msg_)
if not _ABC2MIDI.exists():
    msg_ = f"{_ABC2MIDI} does not exist"
    raise FileNotFoundError(msg_)
# set env var SYMUSIC_MIDI2ABC
os.environ["SYMUSIC_MIDI2ABC"] = str(_MIDI2ABC)
os.environ["SYMUSIC_ABC2MIDI"] = str(_ABC2MIDI)

"""
All the Factory classes are initialized when the module is imported.
And the objects are created when the factory is called.
Note that the factory can not be created again by users,
because the factory is not exposed to the users by setting __all__ manually.

The __isinstancecheck__ method is overrided to make isinstance() work.
"""


class TimeUnitFactory:
    def __init__(self) -> None:
        self._tick = core.Tick()
        self._quarter = core.Quarter()
        self._second = core.Second()

    @property
    def tick(self) -> core.Tick:
        return self._tick

    @property
    def quarter(self) -> core.Quarter:
        return self._quarter

    @property
    def second(self) -> core.Second:
        return self._second

    def __call__(self, ttype: smt.TimeUnit | str) -> smt.TimeUnit:
        """Create a TimeUnit object from a str, e.g. 'tick', 'quarter', 'second'
        It is used to dispatch the correct TimeUnit object.
        However, it is recommended to use the `TimeUnit.tick`, `TimeUnit.quarter`, `TimeUnit.second`
        for better performance.
        """
        if isinstance(ttype, str):
            return self.from_str(ttype)
        try:
            ttype.is_time_unit()
            return ttype
        except AttributeError as e:
            msg = f"{ttype} is not a TimeUnit object"
            raise TypeError(msg) from e

    def from_str(self, ttype: str) -> smt.TimeUnit:
        ttype = ttype.lower()
        if ttype == "tick":
            return self.tick
        if ttype == "quarter":
            return self.quarter
        if ttype == "second":
            return self.second
        msg = f"Invalid time unit: {ttype}"
        raise ValueError(msg)


TimeUnit = TimeUnitFactory()
T = TypeVar("T")
Q = TypeVar("Q")
S = TypeVar("S")


@dataclass(frozen=True)
class CoreClasses(Generic[T, Q, S]):
    tick: T
    quarter: Q
    second: S

    def dispatch(
        self: CoreClasses[T, Q, S],
        ttype: smt.GeneralTimeUnit,
    ) -> T | Q | S:
        """Dispatch the correct Core class according to the ttype."""
        if isinstance(ttype, core.Tick):
            return self.tick
        if isinstance(ttype, core.Quarter):
            return self.quarter
        if isinstance(ttype, core.Second):
            return self.second
        if not isinstance(ttype, str):
            raise ValueError(_ := f"Invalid time unit: {ttype}")
        # ttype can only be str now, while the type checker does not know it.
        ttype: str = ttype.lower()  # type: ignore
        if ttype == "tick":
            return self.tick
        if ttype == "quarter":
            return self.quarter
        if ttype == "second":
            return self.second
        msg = f"Invalid time unit: {ttype}"
        raise ValueError(msg)

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, (self.tick, self.quarter, self.second))  # type: ignore


@dataclass(frozen=True)
class NoteFactory:
    __core_classes = CoreClasses(core.NoteTick, core.NoteQuarter, core.NoteSecond)
    __core_lists = CoreClasses(
        core.NoteTickList,
        core.NoteQuarterList,
        core.NoteSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        duration: smt.TimeDtype,
        pitch: int,
        velocity: int,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Note:
        """Note that `smt.TimeDtype = Union[int, float]`, and Note constructor requires
        `int` or `float` as time. So Type Checker like MyPy will complain about the
        type of `time` argument. However, float and int can be converted to each other
        implicitly. So I just add a `# type: ignore` to ignore the type checking.
        """
        return self.__core_classes.dispatch(ttype)(time, duration, pitch, velocity)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        duration: ndarray,
        pitch: ndarray,
        velocity: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralNoteList:
        return self.__core_lists.dispatch(ttype).from_numpy(
            time,
            duration,
            pitch,
            velocity,
        )


@dataclass(frozen=True)
class KeySignatureFactory:
    __core_classes = CoreClasses(
        core.KeySignatureTick,
        core.KeySignatureQuarter,
        core.KeySignatureSecond,
    )
    __core_lists = CoreClasses(
        core.KeySignatureTickList,
        core.KeySignatureQuarterList,
        core.KeySignatureSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        key: int,
        tonality: int,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.KeySignature:
        return self.__core_classes.dispatch(ttype)(time, key, tonality)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        key: ndarray,
        tonality: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralKeySignatureList:
        return self.__core_lists.dispatch(ttype).from_numpy(time, key, tonality)


@dataclass(frozen=True)
class TimeSignatureFactory:
    __core_classes = CoreClasses(
        core.TimeSignatureTick,
        core.TimeSignatureQuarter,
        core.TimeSignatureSecond,
    )
    __core_lists = CoreClasses(
        core.TimeSignatureTickList,
        core.TimeSignatureQuarterList,
        core.TimeSignatureSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        numerator: int,
        denominator: int,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.TimeSignature:
        return self.__core_classes.dispatch(ttype)(time, numerator, denominator)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        numerator: ndarray,
        denominator: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralTimeSignatureList:
        return self.__core_lists.dispatch(ttype).from_numpy(
            time,
            numerator,
            denominator,
        )


@dataclass(frozen=True)
class ControlChangeFactory:
    __core_classes = CoreClasses(
        core.ControlChangeTick,
        core.ControlChangeQuarter,
        core.ControlChangeSecond,
    )
    __core_lists = CoreClasses(
        core.ControlChangeTickList,
        core.ControlChangeQuarterList,
        core.ControlChangeSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        number: int,
        value: int,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.ControlChange:
        return self.__core_classes.dispatch(ttype)(time, number, value)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        number: ndarray,
        value: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralControlChangeList:
        return self.__core_lists.dispatch(ttype).from_numpy(time, number, value)


@dataclass(frozen=True)
class TempoFactory:
    __core_classes = CoreClasses(core.TempoTick, core.TempoQuarter, core.TempoSecond)
    __core_lists = CoreClasses(
        core.TempoTickList,
        core.TempoQuarterList,
        core.TempoSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        qpm: float | None = None,
        mspq: int | None = None,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Tempo:
        """:param time: the time of the tempo change, in the unit of `ttype`
        :param qpm: quarter per minute. The `bpm` in miditoolkit is actually quarter per minute, not beat per minute.
        :param mspq: microsecond per quarter. We store mspq instead of qpm to avoid float precision problem.
        :param ttype: the time unit of `time`
        :return:
        """
        return self.__core_classes.dispatch(ttype)(time, qpm, mspq)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        mspq: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralTempoList:
        return self.__core_lists.dispatch(ttype).from_numpy(time, mspq)


@dataclass(frozen=True)
class PedalFactory:
    __core_classes = CoreClasses(core.PedalTick, core.PedalQuarter, core.PedalSecond)
    __core_lists = CoreClasses(
        core.PedalTickList,
        core.PedalQuarterList,
        core.PedalSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        duration: smt.TimeDtype,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Pedal:
        return self.__core_classes.dispatch(ttype)(time, duration)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        duration: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralPedalList:
        return self.__core_lists.dispatch(ttype).from_numpy(time, duration)


@dataclass(frozen=True)
class PitchBendFactory:
    __core_classes = CoreClasses(
        core.PitchBendTick,
        core.PitchBendQuarter,
        core.PitchBendSecond,
    )
    __core_lists = CoreClasses(
        core.PitchBendTickList,
        core.PitchBendQuarterList,
        core.PitchBendSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        value: int,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.PitchBend:
        return self.__core_classes.dispatch(ttype)(time, value)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        value: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralPitchBendList:
        return self.__core_lists.dispatch(ttype).from_numpy(time, value)


@dataclass(frozen=True)
class TextMetaFactory:
    __core_classes = CoreClasses(
        core.TextMetaTick,
        core.TextMetaQuarter,
        core.TextMetaSecond,
    )
    __core_lists = CoreClasses(
        core.TextMetaTickList,
        core.TextMetaQuarterList,
        core.TextMetaSecondList,
    )

    def __call__(
        self,
        time: smt.TimeDtype,
        text: str,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.TextMeta:
        return self.__core_classes.dispatch(ttype)(time, text)  # type: ignore

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def from_numpy(
        self,
        time: ndarray,
        text: ndarray,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.GeneralTextMetaList:
        raise NotImplementedError
        # return self.__core_classes.dispatch(ttype).from_numpy(time, text)


@dataclass(frozen=True)
class TrackFactory:
    __core_classes = CoreClasses(core.TrackTick, core.TrackQuarter, core.TrackSecond)

    def __call__(
        self,
        name: str = "",
        program: int = 0,
        is_drum: bool = False,
        notes: smt.GeneralNoteList = None,
        controls: smt.GeneralControlChangeList = None,
        pitch_bends: smt.GeneralPitchBendList = None,
        pedals: smt.GeneralPedalList = None,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Track:
        r"""Create a Track object with the given parameters.
        Note that all of these parameters are optional,
        and they will be copied to the new Track object.
        So it is safe to use `[]` in the default value.

        Of course, copy will cause a little overhead, but it is acceptable.
        And create a `Note` object (bound by pybind11) is much more expensive.
        """
        new_track = self.empty(ttype)
        new_track.name = name
        new_track.program = program
        new_track.is_drum = is_drum
        new_track.notes = notes if notes else []
        new_track.controls = controls if controls else []
        new_track.pitch_bends = pitch_bends if pitch_bends else []
        new_track.pedals = pedals if pedals else []
        return new_track

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore

    def empty(self, ttype: smt.GeneralTimeUnit = "tick") -> smt.Track:
        # create an empty track
        return self.__core_classes.dispatch(ttype)()


@dataclass(frozen=True)
class ScoreFactory:
    __core_classes = CoreClasses(core.ScoreTick, core.ScoreQuarter, core.ScoreSecond)

    def __call__(
        self,
        x: int | str | Path | smt.Score = 960,
        ttype: smt.GeneralTimeUnit = "tick",
        fmt: str | None = None,
    ) -> smt.Score:
        if isinstance(x, (str, Path)):
            return self.from_file(x, ttype, fmt)
        if isinstance(x, int):
            return self.from_tpq(x, ttype)
        if isinstance(x, self):  # type: ignore
            return self.from_other(x, ttype)
        msg = f"Invalid type: {type(x)}"
        raise TypeError(msg)

    def from_file(
        self,
        path: str | Path,
        ttype: smt.GeneralTimeUnit = "tick",
        fmt: str | None = None,
    ) -> smt.Score:
        if isinstance(path, str):
            path = Path(path)
        if not path.is_file():
            raise ValueError(_ := f"{path} is not a file")
        return self.__core_classes.dispatch(ttype).from_file(path, fmt)

    def from_midi(
        self,
        data: bytes,
        ttype: smt.GeneralTimeUnit = "tick",
        strict_mode: bool = True,
    ) -> smt.Score:
        return self.__core_classes.dispatch(ttype).from_midi(data, strict_mode)

    def from_abc(
        self,
        abc: str,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Score:
        return self.__core_classes.dispatch(ttype).from_abc(abc)

    def from_tpq(
        self,
        tpq: int = 960,
        ttype: smt.GeneralTimeUnit = "tick",
    ) -> smt.Score:
        return self.__core_classes.dispatch(ttype)(tpq)

    def from_other(
        self,
        other: smt.Score,
        ttype: smt.GeneralTimeUnit = "tick",
        min_dur: int | None = None,
    ) -> smt.Score:
        if other.ticks_per_quarter <= 0:
            msg = (
                f"ticks_per_quarter must be positive, but got {other.ticks_per_quarter}"
            )
            raise ValueError(
                msg,
            )
        return self.__core_classes.dispatch(ttype)(other, min_dur)

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.__core_classes)  # type: ignore


class SynthesizerFactory:
    def __call__(
        self,
        sf_path: str | Path | None = None,
        sample_rate: int = 44100,
        quality: int = 0,
    ):
        if sf_path is None:
            sf_path = BuiltInSF3.MuseScoreGeneral().path(download=True)
        sf_path = str(sf_path)
        return core.Synthesizer(sf_path, sample_rate, quality)

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, core.Synthesizer)


Note = NoteFactory()
KeySignature = KeySignatureFactory()
TimeSignature = TimeSignatureFactory()
ControlChange = ControlChangeFactory()
Tempo = TempoFactory()
Pedal = PedalFactory()
PitchBend = PitchBendFactory()
TextMeta = TextMetaFactory()
Track = TrackFactory()
Score = ScoreFactory()
Synthesizer = SynthesizerFactory()

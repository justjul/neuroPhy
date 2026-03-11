"""
experiment.py

Core data structures for neuroPhy sessions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar

from .params.analysis_params import (
    DecoderParameters,
    GLMParameters,
    MapParameters,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _has_content(value: Any) -> bool:
    if value is None:
        return False

    if isinstance(value, (dict, list, tuple, set, str, bytes)):
        return len(value) > 0

    size = getattr(value, "size", None)
    if isinstance(size, int):
        return size > 0

    try:
        return bool(value)
    except Exception:
        return True


# ---------------------------------------------------------------------------
# Flat modality dictionaries
# ---------------------------------------------------------------------------

class ModalityDict(dict):
    """
    Flat dict-like container for one modality.

    Standard fields are initialized to None, but arbitrary experiment-specific
    fields may be added freely.
    """

    standard_fields: ClassVar[tuple[str, ...]] = ()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        for key in self.standard_fields:
            self[key] = None
        self.update(*args, **kwargs)

    def is_loaded(self) -> bool:
        return any(_has_content(v) for v in self.values())


class BehData(ModalityDict):
    standard_fields = (
        "sampleTimes",
        "trials",
        "fs",
    )


class SpkData(ModalityDict):
    standard_fields = (
        "spikeTimes",
        "unitIds",
        "channelIds",
        "probeIds",
        "quality",
        "brain_region",
    )


class LfpData(ModalityDict):
    standard_fields = (
        "sampleTimes",
        "signal",
        "fs",
        "channelIds",
        "probeIds",
    )


class StmData(ModalityDict):
    standard_fields = (
        "stimTimes",
        "stimIds",
        "stimParams",
    )


# ---------------------------------------------------------------------------
# Result objects
# ---------------------------------------------------------------------------

@dataclass
class MapResult:
    name: str
    params: MapParameters | None = None
    tuning: dict[str, Any] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)

    def is_loaded(self) -> bool:
        return any(_has_content(v) for v in (self.tuning, self.stats))


@dataclass
class GLMResult:
    name: str
    params: GLMParameters | None = None
    tuning: dict[str, Any] = field(default_factory=dict)
    perf: Any | None = None
    stats: dict[str, Any] = field(default_factory=dict)

    def is_loaded(self) -> bool:
        return any(_has_content(v) for v in (self.tuning, self.perf, self.stats))


@dataclass
class DecoderResult:
    name: str
    params: DecoderParameters | None = None
    decoded: dict[str, Any] = field(default_factory=dict)
    posterior: dict[str, Any] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)

    def is_loaded(self) -> bool:
        return any(_has_content(v) for v in (self.decoded, self.posterior, self.stats))


# ---------------------------------------------------------------------------
# Stores
# ---------------------------------------------------------------------------

@dataclass
class SessionInfo:
    projectDIR: str | None = None
    animal: str | None = None
    series: str | None = None
    exp: list[str] | None = None
    procFiles_path: str | None = None


@dataclass
class DataStore:
    Beh: BehData = field(default_factory=BehData)
    Spk: SpkData = field(default_factory=SpkData)
    Lfp: LfpData = field(default_factory=LfpData)
    Stm: StmData = field(default_factory=StmData)


@dataclass
class ResultsStore:
    maps: dict[str, MapResult] = field(default_factory=dict)
    glms: dict[str, GLMResult] = field(default_factory=dict)
    decoders: dict[str, DecoderResult] = field(default_factory=dict)
    custom: dict[str, Any] = field(default_factory=dict)

    def add_map(self, result: MapResult) -> None:
        self.maps[result.name] = result

    def add_glm(self, result: GLMResult) -> None:
        self.glms[result.name] = result

    def add_decoder(self, result: DecoderResult) -> None:
        self.decoders[result.name] = result

    def add_custom(self, name: str, result: Any) -> None:
        self.custom[name] = result


# ---------------------------------------------------------------------------
# Top-level EXP container
# ---------------------------------------------------------------------------

@dataclass
class EXP:
    info: SessionInfo = field(default_factory=SessionInfo)
    data: DataStore = field(default_factory=DataStore)
    results: ResultsStore = field(default_factory=ResultsStore)

    @classmethod
    def from_saved(cls, saved: dict[str, Any]) -> EXP:
        instance = cls()

        if "info" in saved:
            instance.info = SessionInfo(**saved["info"])

        if "data" in saved:
            data = saved["data"]
            if "Beh" in data:
                instance.data.Beh = _build_modality_dict(BehData, data["Beh"])
            if "Spk" in data:
                instance.data.Spk = _build_modality_dict(SpkData, data["Spk"])
            if "Lfp" in data:
                instance.data.Lfp = _build_modality_dict(LfpData, data["Lfp"])
            if "Stm" in data:
                instance.data.Stm = _build_modality_dict(StmData, data["Stm"])

        if "results" in saved:
            results = saved["results"]

            for name, val in results.get("maps", {}).items():
                instance.results.maps[name] = val if isinstance(
                    val, MapResult) else MapResult(**val)

            for name, val in results.get("glms", {}).items():
                instance.results.glms[name] = val if isinstance(
                    val, GLMResult) else GLMResult(**val)

            for name, val in results.get("decoders", {}).items():
                instance.results.decoders[name] = val if isinstance(
                    val, DecoderResult) else DecoderResult(**val)

            instance.results.custom = results.get("custom", {})

        return instance

    def update_from_saved(self, saved: dict[str, Any]) -> None:
        updated = self.from_saved(saved)
        self.info = updated.info
        self.data = updated.data
        self.results = updated.results

    def to_dict(self) -> dict[str, Any]:
        return {
            "info": asdict(self.info),
            "data": {
                "Beh": dict(self.data.Beh),
                "Spk": dict(self.data.Spk),
                "Lfp": dict(self.data.Lfp),
                "Stm": dict(self.data.Stm),
            },
            "results": {
                "maps": {k: asdict(v) for k, v in self.results.maps.items()},
                "glms": {k: asdict(v) for k, v in self.results.glms.items()},
                "decoders": {k: asdict(v) for k, v in self.results.decoders.items()},
                "custom": self.results.custom,
            },
        }

    def summary(self) -> str:
        lines = [
            "EXP Session Summary",
            "===================",
            f"Project  : {self.info.projectDIR}",
            f"Animal   : {self.info.animal}",
            f"Series   : {self.info.series}",
            f"Exp      : {self.info.exp}",
            f"ProcPath : {self.info.procFiles_path}",
            "",
            f"Beh loaded      : {'yes' if self.data.Beh.is_loaded() else 'no'}",
            f"Spk loaded      : {'yes' if self.data.Spk.is_loaded() else 'no'}",
            f"Lfp loaded      : {'yes' if self.data.Lfp.is_loaded() else 'no'}",
            f"Stm loaded      : {'yes' if self.data.Stm.is_loaded() else 'no'}",
            "",
            f"Maps results    : {len(self.results.maps)}",
            f"GLMs results    : {len(self.results.glms)}",
            f"Decoders results: {len(self.results.decoders)}",
            f"Custom results  : {len(self.results.custom)}",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"EXP(animal={self.info.animal!r}, "
            f"series={self.info.series!r}, "
            f"exp={self.info.exp!r})"
        )


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def _build_modality_dict(cls_: type[ModalityDict], saved: Any) -> ModalityDict:
    if isinstance(saved, cls_):
        return saved

    if isinstance(saved, dict):
        return cls_(saved)

    raise TypeError(f"Cannot rebuild {cls_.__name__} from type {type(saved)}")

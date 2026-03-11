"""
data_structures.py

Core data structure for neuroPhy sessions.

Data are grouped by modality:
    - Beh  : behavioral data (navigation, position, speed, etc.)
    - Spk  : spike / unit data
    - Lfp  : local field potential data
    - Stm  : visual / sensory stimulus data

Analysis results are stored in:
    - Maps : spatial / tuning maps
    - GLMs  : generalized linear model results
    - OptiMaps : cross-validated spatial / tuning maps
    - Decoders : decoding analysis results
    - Custom   : user-defined analysis outputs
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any

# ---------------------------------------------------------------------------
# Sub-structure placeholders
# Each sub-structure is intentionally kept as a lightweight container so that
# the loader functions (LoadNavData, LoadSpkData, …) can populate them freely.
# ---------------------------------------------------------------------------


@dataclass
class BehData:
    """Behavioral / navigation data container."""
    # Common behavioral signals — populated by the loader
    sampleTime:       Any | None = None   # timestamps (s)
    position:   Any | None = None   # (x, y) trajectory
    speed:      Any | None = None   # instantaneous speed
    direction:  Any | None = None   # heading angle
    trials:     Any | None = None   # trial / lap annotations
    # Catch-all for any extra fields added at load time
    extra: dict = field(default_factory=dict)


@dataclass
class SpkData:
    """Spike / unit data container."""
    spikeTimes:   Any | None = None   # list of arrays, one per unit
    unit_ids:      Any | None = None   # unit labels / cluster ids
    waveforms:     Any | None = None   # mean waveforms
    quality:       Any | None = None   # isolation quality metrics
    brain_region:  Any | None = None   # anatomical tags
    extra: dict = field(default_factory=dict)


@dataclass
class LfpData:
    """Local field potential data container."""
    sampleTime:        Any | None = None   # timestamps (s)
    signal:      Any | None = None   # (n_channels × n_samples) array
    fs:          Any | None = None  # sampling rate (Hz)
    channel_ids: Any | None = None   # channel labels
    brain_region: Any | None = None
    extra: dict = field(default_factory=dict)


@dataclass
class StmData:
    """Visual / sensory stimulus data container."""
    stimTimes:  Any | None = None   # stimulus onset times
    stim_ids:    Any | None = None   # stimulus identities
    stim_params: Any | None = None   # stimulus parameters dict
    extra: dict = field(default_factory=dict)


@dataclass
class mapsData:
    """Cross-validated spatial / tuning maps container."""
    place_fields:   Any | None = None
    rate_maps:      Any | None = None
    tuning_curves:  Any | None = None
    cv_scores:      Any | None = None   # cross-validation scores
    extra: dict = field(default_factory=dict)


@dataclass
class glmsData:
    """Cross-validated spatial / tuning maps container."""
    place_fields:   Any | None = None
    rate_maps:      Any | None = None
    tuning_curves:  Any | None = None
    cv_scores:      Any | None = None   # cross-validation scores
    extra: dict = field(default_factory=dict)


@dataclass
class decodersData:
    """Decoding analysis results container."""
    decoded_position: Any | None = None
    decoded_variable: Any | None = None
    decoder_type:     Any | None = None
    performance:      Any | None = None   # accuracy / error metrics
    extra: dict = field(default_factory=dict)


@dataclass
class customData:
    """User-defined analysis outputs."""
    extra: dict = field(default_factory=dict)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow arbitrary attributes, storing unknowns in `extra`
        if name == "extra" or name in {f.name for f in fields(self)}:
            super().__setattr__(name, value)
        else:
            self.extra[name] = value

    def __getattr__(self, name: str) -> Any:
        try:
            return self.extra[name]
        except KeyError:
            raise AttributeError(
                f"CustomData has no attribute '{name}'") from None


# ---------------------------------------------------------------------------
# Top-level EXP session structure
# ---------------------------------------------------------------------------

@dataclass
class EXP:
    """
    Top-level session container, equivalent to the MATLAB EXP / Tstructure.

    Parameters
    ----------
    projectDIR : str | Path
        Root directory of the project.
    animal : str
        Animal / subject identifier.
    series : str
        Recording series identifier.
    exp : list[str]
        Experiment / session identifier.
    procFiles_path : str | Path, optional
        Path to processed data files.

    Data modalities
    ---------------
    Beh       : BehData
    Spk       : SpkData
    Lfp       : LfpData
    Stm       : StmData

    Analysis results
    ----------------
    Maps      : mapsData
    GLMs      : glmsData
    OptiMaps  : mapsData
    Decoders  : decodersData
    Custom    : customData
    """

    # Session metadata
    projectDIR:     str | None = None
    animal:         str | None = None
    series:         str | None = None
    exp:            list[str] | None = None
    procFiles_path: str | None = None

    # Data modalities
    Beh:      BehData = field(default_factory=BehData)
    Spk:      SpkData = field(default_factory=SpkData)
    Lfp:      LfpData = field(default_factory=LfpData)
    Stm:      StmData = field(default_factory=StmData)

    # Analysis results
    Maps: mapsData = field(default_factory=mapsData)
    GLMs: glmsData = field(default_factory=glmsData)
    OptiMaps: mapsData = field(default_factory=mapsData)
    Decoders: decodersData = field(default_factory=decodersData)
    Custom:   customData = field(default_factory=customData)

    # -----------------------------------------------------------------------
    # Class methods
    # -----------------------------------------------------------------------

    @classmethod
    def from_saved(cls, saved: dict) -> EXP:
        """
        Reconstruct an EXP from a previously saved dictionary (e.g. loaded
        from JSON / pickle), copying matching top-level fields.

        Mirrors MATLAB's UpdateEXPstructure(EXP, savedEXP) behaviour.
        """
        instance = cls()
        _PROP_LIST = {f.name for f in fields(cls)}

        for key, value in saved.items():
            if key in _PROP_LIST:
                setattr(instance, key, value)

        return instance

    def update_from_saved(self, saved: dict) -> None:
        """
        In-place update from a saved dict — equivalent to calling
        UpdateEXPstructure(EXP, savedEXP) on an existing object.
        """
        _PROP_LIST = {f.name for f in fields(self)}
        for key, value in saved.items():
            if key in _PROP_LIST:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        """Serialize the full EXP structure to a nested dictionary."""
        return asdict(self)

    def summary(self) -> str:
        """Return a human-readable summary of the session."""
        lines = [
            "EXP Session Summary",
            "===================",
            f"  Project  : {self.projectDIR}",
            f"  Animal   : {self.animal}",
            f"  Series   : {self.series}",
            f"  Exp      : {self.exp}",
            f"  ProcPath : {self.procFiles_path}",
            "",
            "  Beh      loaded: " + _loaded_flag(self.Beh),
            "  Spk      loaded: " + _loaded_flag(self.Spk),
            "  Lfp      loaded: " + _loaded_flag(self.Lfp),
            "  Stm      loaded: " + _loaded_flag(self.Stm),
            "  OptiMaps loaded: " + _loaded_flag(self.OptiMaps),
            "  Decoders loaded: " + _loaded_flag(self.Decoders),
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"EXP(animal={self.animal!r}, series={self.series!r}, "
            f"exp={self.exp!r})"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _loaded_flag(sub: Any) -> str:
    """Return 'yes' if any field of a sub-structure is non-None / non-empty."""
    for f in fields(sub):
        val = getattr(sub, f.name)
        if val is not None and val != {}:
            return "yes"
    return "no"

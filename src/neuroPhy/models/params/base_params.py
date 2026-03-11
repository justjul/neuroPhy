from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .analysis_params import (
    CustomParameters,
    DecoderParameters,
    GLMParameters,
    MapParameters,
    OutputParameters,
    PredictorParameters,
)
from .load_params import LoadParameters
from .plot_params import PlotParametersBehavior, PlotParametersCells, PlotParametersDecoder

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_N_PREDICTORS = 10  # maximum number of predictors in GLM / Decoder


def _build_predictor(data: dict | None) -> PredictorParameters:
    """Safely construct a PredictorParameters from a dict (or return default)."""
    if not data:
        return PredictorParameters()
    return PredictorParameters(**data)


def _build_output(data: dict | None) -> OutputParameters:
    """Safely construct an OutputParameters from a dict (or return default)."""
    if not data:
        return OutputParameters()
    return OutputParameters(**data)


def _build_predictors_list(data: list[dict] | None) -> list[PredictorParameters]:
    """
    Build a fixed-length list of PredictorParameters.

    Extra entries beyond _N_PREDICTORS are silently truncated.
    Missing entries (list shorter than _N_PREDICTORS) are padded with defaults.
    """
    result: list[PredictorParameters] = []
    for item in (data or []):
        result.append(_build_predictor(item))
    # Pad to _N_PREDICTORS with default (empty) predictors
    while len(result) < _N_PREDICTORS:
        result.append(PredictorParameters())
    return result[:_N_PREDICTORS]


def _build_map_params(data: dict) -> MapParameters:
    d = dict(data)
    predictor = _build_predictor(d.pop("predictor", None))
    output = _build_output(d.pop("output", None))
    return MapParameters(predictor=predictor, output=output, **d)


def _build_glm_params(data: dict) -> GLMParameters:
    d = dict(data)
    predictors = _build_predictors_list(d.pop("predictors", None))
    output = _build_output(d.pop("output", None))
    return GLMParameters(predictors=predictors, output=output, **d)


def _build_decoder_params(data: dict) -> DecoderParameters:
    d = dict(data)
    predictors = _build_predictors_list(d.pop("predictors", None))
    output = _build_output(d.pop("output", None))
    return DecoderParameters(predictors=predictors, output=output, **d)


# ---------------------------------------------------------------------------
# Top-level Parameters container
# ---------------------------------------------------------------------------

@dataclass
class Parameters:
    """
    Main parameter configuration container for neuroPhy.

    Holds all parameters for loading data, running analyses, and rendering
    visualizations. Can be serialized to / deserialized from YAML.

    Usage
    -----
    >>> # Load from the default params.yaml at project root
    >>> params = Parameters.from_default()

    >>> # Load from an explicit file
    >>> params = Parameters.from_yaml('/path/to/my_params.yaml')

    >>> # Persist modifications
    >>> params.to_yaml('my_params.yaml')

    Attributes
    ----------
    load_params : LoadParameters
        Data loading configuration (paths, sync signal, subset filters).
    maps_params : list[MapParameters]
        Cross-validated spatial / tuning map configurations.
        Each entry owns a single PredictorParameters + OutputParameters.
    glms_params : list[GLMParameters]
        Generalized Linear Model configurations.
        Each entry owns up to 10 PredictorParameters + OutputParameters.
    decoders_params : list[DecoderParameters]
        Bayesian / linear / ANN decoder configurations.
        Each entry owns up to 10 PredictorParameters + OutputParameters.
    custom_params : list[CustomParameters]
        User-defined analysis configurations.
    plot_params_cells : PlotParametersCells
        Single-cells page visualization settings.
    plot_params_decoder : PlotParametersDecoder
        Decoder page visualization settings.
    plot_params_behavior : PlotParametersBehavior
        Behavior page visualization settings.
    """

    load_params: LoadParameters = field(default_factory=LoadParameters)
    maps_params: list[MapParameters] = field(default_factory=list)
    glms_params: list[GLMParameters] = field(default_factory=list)
    decoders_params: list[DecoderParameters] = field(default_factory=list)
    custom_params: list[CustomParameters] = field(default_factory=list)
    plot_params_cells: PlotParametersCells = field(
        default_factory=PlotParametersCells)
    plot_params_decoder: PlotParametersDecoder = field(
        default_factory=PlotParametersDecoder)
    plot_params_behavior: PlotParametersBehavior = field(
        default_factory=PlotParametersBehavior)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a nested plain dictionary (YAML-ready)."""
        return asdict(self)

    def to_yaml(self, filepath: str) -> None:
        """
        Save parameters to a YAML file.

        Parameters
        ----------
        filepath : str
            Destination path.
        """
        with open(filepath, "w") as f:
            yaml.dump(self.to_dict(), f,
                      default_flow_style=False, sort_keys=False)
        print(f"Parameters saved to {filepath}")

    # ------------------------------------------------------------------
    # Deserialization
    # ------------------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Parameters":
        """
        Reconstruct a Parameters object from a plain dictionary.

        Handles nested dataclasses (PredictorParameters, OutputParameters, …)
        so that a dict produced by to_dict() or loaded from YAML round-trips
        correctly.

        Parameters
        ----------
        data : dict
            Flat or nested dictionary (e.g. parsed from YAML).

        Returns
        -------
        Parameters
        """
        load_params = LoadParameters(**data.get("load_params", {}))

        maps_params = [
            _build_map_params(mp) for mp in data.get("maps_params", [])
        ]
        glms_params = [
            _build_glm_params(gp) for gp in data.get("glms_params", [])
        ]
        decoders_params = [
            _build_decoder_params(dp) for dp in data.get("decoders_params", [])
        ]
        custom_params = [
            CustomParameters(**cp) for cp in data.get("custom_params", [])
        ]

        plot_params_cells = PlotParametersCells(
            **data.get("plot_params_cells", {}))
        plot_params_decoder = PlotParametersDecoder(
            **data.get("plot_params_decoder", {}))
        plot_params_behavior = PlotParametersBehavior(
            **data.get("plot_params_behavior", {}))

        return cls(
            load_params=load_params,
            maps_params=maps_params,
            glms_params=glms_params,
            decoders_params=decoders_params,
            custom_params=custom_params,
            plot_params_cells=plot_params_cells,
            plot_params_decoder=plot_params_decoder,
            plot_params_behavior=plot_params_behavior,
        )

    @classmethod
    def from_yaml(cls, filepath: str) -> "Parameters":
        """
        Load parameters from a YAML file.

        Parameters
        ----------
        filepath : str
            Path to the YAML file.

        Returns
        -------
        Parameters

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        yaml.YAMLError
            If the file is not valid YAML.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Parameters file not found: {path}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data or {})

    @classmethod
    def from_default(cls) -> "Parameters":
        """
        Load parameters from the default params.yaml at the project root.

        The project root is inferred by walking up from this file's location:
        src/neuroPhy/core/params/base_params.py → project root (4 levels up).

        Returns
        -------
        Parameters

        Raises
        ------
        FileNotFoundError
            If params.yaml is not found at the expected location.
        """
        project_root = Path(__file__).parents[4]
        default_path = project_root / "params.yaml"

        if not default_path.exists():
            raise FileNotFoundError(
                f"Default params.yaml not found at {default_path}. "
                "Copy params.example.yaml and fill in your paths."
            )

        return cls.from_yaml(str(default_path))

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a human-readable summary of the current configuration."""
        lines = [
            "=" * 50,
            "neuroPhy Parameters Summary",
            "=" * 50,
            f"\nProject : {self.load_params.project_dir}",
            f"Animal  : {getattr(self.load_params, 'animal', None) or '(not set)'}",
            f"Series  : {getattr(self.load_params, 'series', None) or '(not set)'}",
            f"Exp     : {getattr(self.load_params, 'exp', None) or '(not set)'}",
            "\nAnalysis configurations:",
            f"  Maps     : {len(self.maps_params)}",
            f"  GLMs     : {len(self.glms_params)}",
            f"  Decoders : {len(self.decoders_params)}",
            f"  Custom   : {len(self.custom_params)}",
            "=" * 50,
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

def load_params(filepath: str = "params.yaml") -> Parameters:
    """Load parameters from a YAML file (default: 'params.yaml')."""
    return Parameters.from_yaml(filepath)


def save_params(params: Parameters, filepath: str = "params.yaml") -> None:
    """Save parameters to a YAML file (default: 'params.yaml')."""
    params.to_yaml(filepath)


if __name__ == "__main__":
    try:
        params = Parameters.from_default()
        print(params.summary())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Create a params.yaml from the template before running.")

"""
Parameter structures for neuroPhy plotting tools

Defines parameter classes for configuring visualizations such as single cell plots, decoder results, and behavioral trajectories.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlotParametersCells:
    """
    Parameters for single cells plotting page

    Controls UI layout and plotting options for visualizing single cell data.

    Layout:
        PageTitle: Display name for the page
        Page: Page number (tab position)
        DialogWindow: Dialog position (1=left, 2=right)
        Window: Plot area position (1=right, 2=left)
        Foverlap: Whether to overlap plots in same axes

    Visualization:
        colormap: Colormap for matrices and multi-line plots
        ChosenCell: Selected cell ID(s) to display
        FpoolCell: Pool spikes from multiple cells

    Variable Selection:
        ChosenVar*origin: Origin fields for X, Y, C variables
        ChosenVar*name: Field names for X, Y, C variables

    Plot Objects:
        PlotObjList: Available plot types [name, selected, function, params...]

    Data Filtering:
        Dialog_params: Subset conditions shown in dialog
        fixed_params: Fixed subset conditions (not shown)
    """
    PageTitle: str = "Single Cells"
    Page: int = 1
    DialogWindow: int = 1
    Window: int = 2
    Foverlap: bool = False
    colormap: str = "hot"
    ChosenCell: int | list[int] = 1
    FpoolCell: bool = False
    ChosenVarXorigin: str = "Beh"
    ChosenVarXname: str = "XPercent"
    ChosenVarYorigin: str = "Beh"
    ChosenVarYname: str = "YPercent"
    ChosenVarCorigin: str = "Beh"
    ChosenVarCname: str = "none"
    PlotObjList: list[list[Any]] = field(default_factory=list)
    Dialog_params: list[list[Any]] = field(default_factory=list)
    fixed_params: list[list[Any]] = field(default_factory=list)


@dataclass
class PlotParametersDecoder:
    """
    Parameters for decoding results plotting page

    Similar to PlotParametersCells but specialized for decoder outputs.

    Additional Attributes:
        Clim: [min, max] Z-axis limits for matrix plots
        Flogscale: Use log2 scale for Z values
        Xsmthwin: Spatial smoothing window size
        Predictor_params: Predictor subset conditions
    """
    PageTitle: str = "Decoding"
    Page: int = 2
    DialogWindow: int = 1
    Window: int = 2
    Foverlap: bool = False
    Clim: list[float] = field(default_factory=lambda: [0.0, 2.0])
    Flogscale: bool = False
    colormap: str = "RedWhiteBlue"
    Xsmthwin: float = 2.0
    PlotObjList: list[list[Any]] = field(default_factory=list)
    Dialog_params: list[list[Any]] = field(default_factory=list)
    Predictor_params: list[list[Any]] = field(default_factory=list)
    fixed_params: list[list[Any]] = field(default_factory=list)


@dataclass
class PlotParametersBehavior:
    """
    Parameters for behavioral data plotting page

    Specialized for visualizing behavioral trajectories and events.

    Additional Attributes:
        PlotLick: Lick event display options [name, show, [R,G,B]]
    """
    PageTitle: str = "Behavior"
    Page: int = 3
    DialogWindow: int = 1
    Window: int = 2
    Foverlap: bool = False
    colormap: str = "cool"
    ChosenVarXorigin: str = "Beh"
    ChosenVarXname: str = "XPercent"
    ChosenVarYorigin: str = "Beh"
    ChosenVarYname: str = "YPercent"
    PlotLick: list[list[Any]] = field(default_factory=list)
    PlotObjList: list[list[Any]] = field(default_factory=list)
    Dialog_params: list[list[Any]] = field(default_factory=list)
    fixed_params: list[list[Any]] = field(default_factory=list)

"""
Parameter structures for neuroPhy analysis tools

Defines parameter classes for configuring analyses such as spatial maps,
GLMs, and decoders.

Class hierarchy
---------------
PredictorParameters
    Encapsulates one predictor variable with up to three spatial axes (X, Y, Z)
    and optional temporal parameters. Used both as the single predictor in
    MapParameters and as elements of the predictors list in GLMParameters /
    DecoderParameters.

OutputParameters
    Encapsulates the response / output variable and its optional subset
    conditions.

MapParameters
    Configuration for one cross-validated spatial / tuning map.
    Holds exactly one PredictorParameters + one OutputParameters.

GLMParameters
    Configuration for one GLM analysis.
    Holds up to 10 PredictorParameters + one OutputParameters.

DecoderParameters
    Configuration for one decoding analysis (Bayesian, Linear, or ANN).
    Holds up to 10 PredictorParameters (decoded variables) + one
    OutputParameters (neural predictor).

CustomParameters
    Configuration for a user-defined analysis function.
"""

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# PredictorParameters
# ---------------------------------------------------------------------------

@dataclass
class PredictorParameters:
    """
    Parameters for a single predictor variable.

    A predictor can have up to three spatial / feature axes (X, Y, Z) and an
    optional temporal dimension.  Each axis is independently configured with
    its data source, discretisation, and handling flags.

    Used in:
    - MapParameters.predictor   (single predictor for a map)
    - GLMParameters.predictors  (list of up to 10, one per model term)
    - DecoderParameters.predictors (list of up to 10, one per decoded variable)

    X axis
    ------
    Xorigin : str
        EXP field that contains the X variable (e.g. 'Beh', 'Spk', 'none').
    Xname : str
        Field name within Xorigin (e.g. 'XPercent', 'HeadDirection').
    Xbinsize : float | None
        Bin width for discretisation.  Ignored when Xlinear is True.
    XsmthNbins : int | None
        Gaussian smoothing kernel width, in bins.  0 or None = no smoothing.
    Xrange : list[float] | None
        [min, max] clipping / binning range.  None = data-driven range.
    Xbinedges : list[float] | None
        Explicit bin-edge array.  When provided, overrides Xrange + Xbinsize.
    Xcircular : bool
        True if the variable wraps (e.g. head direction in radians).
    Xclamp : bool
        True to clip values to Xrange instead of discarding out-of-range
        samples.
    Xlinear : bool
        True to include this axis as a continuous linear regressor rather than
        a discretised factor.
    Xindexed : bool
        True to treat the values as integer category indices.
    XalwaysIn : bool
        True to force this predictor into every model fold without selection.
    Xremovenan : bool
        True to treat NaN samples as missing and exclude them from the
        analysis (rather than counting them as zero).

    Y axis  (same semantics as X)
    ------
    Yorigin, Yname, Ybinsize, YsmthNbins, Yrange, Ybinedges,
    Ycircular, Yclamp, Ylinear, Yindexed, YalwaysIn, Yremovenan

    Z axis  (same semantics as X)
    ------
    Zorigin, Zname, Zbinsize, ZsmthNbins, Zrange, Zbinedges,
    Zcircular, Zclamp, Zlinear, Zindexed, ZalwaysIn, Zremovenan

    Temporal parameters
    -------------------
    Timerange : float | list[float]
        Single value: fixed time offset (s).
        Two-element list [t_min, t_max]: range of time delays to explore.
        0.0 = no temporal shift.
    Timestep : float
        Step size (s) when exploring a range of time delays.  0.0 = single
        value only.
    TsmthNbins : int
        Temporal smoothing window width in bins applied to this predictor.
        0 = no smoothing.
    """

    # --- X axis ---
    Xorigin: str = "none"           # origin field in EXP ('Beh', 'Spk', …)
    Xname: str = "none"             # variable name within Xorigin
    Xbinsize: float | None = None   # bin width for discretisation
    XsmthNbins: int | None = None   # smoothing kernel width (bins)
    Xrange: list[float] | None = None   # [min, max] range
    # explicit bin edges (overrides range+binsize)
    Xbinedges: list[float] | None = None
    Xcircular: bool = False         # True if variable wraps (e.g. angle)
    Xclamp: bool = False            # True to clip rather than discard out-of-range
    Xlinear: bool = False           # True for continuous linear regressor
    Xindexed: bool = False          # True to treat values as integer categories
    XalwaysIn: bool = False         # True to always include (skip selection)
    # True to exclude NaN samples (not zero-fill)
    Xremovenan: bool = False

    # --- Y axis ---
    Yorigin: str = "none"
    Yname: str = "none"
    Ybinsize: float | None = None
    YsmthNbins: int | None = None
    Yrange: list[float] | None = None
    Ybinedges: list[float] | None = None
    Ycircular: bool = False
    Yclamp: bool = False
    Ylinear: bool = False
    Yindexed: bool = False
    YalwaysIn: bool = False
    Yremovenan: bool = False

    # --- Z axis ---
    Zorigin: str = "none"
    Zname: str = "none"
    Zbinsize: float | None = None
    ZsmthNbins: int | None = None
    Zrange: list[float] | None = None
    Zbinedges: list[float] | None = None
    Zcircular: bool = False
    Zclamp: bool = False
    Zlinear: bool = False
    Zindexed: bool = False
    ZalwaysIn: bool = False
    Zremovenan: bool = False

    # --- Temporal ---
    Timerange: float | list[float] = 0.0   # time offset or [t_min, t_max] (s)
    # step when exploring delay range (s)
    Timestep: float = 0.0
    TsmthNbins: int = 0                    # temporal smoothing width (bins)


# ---------------------------------------------------------------------------
# OutputParameters
# ---------------------------------------------------------------------------

@dataclass
class OutputParameters:
    """
    Parameters for the output / response variable.

    Describes where the response signal lives in the EXP structure and any
    subset conditions that restrict which units / channels are included.

    Attributes
    ----------
    Oorigin : str
        EXP field that contains the output variable (e.g. 'Spk').
    Oname : str
        Field name within Oorigin (e.g. 'spikeTrain').
    OsubsetInfo : list[list]
        Conditions for selecting a subset of output units / channels.
        Each entry is a list: [origin, field, value, operator].
        Example: [['Spk', 'Probe', 1, '=']] selects units from Probe 1.
        An empty list means all units are included.
    """

    Oorigin: str = "Spk"                             # origin field in EXP
    Oname: str = "spikeTrain"                        # variable name within Oorigin
    OsubsetInfo: list[list[Any]] = field(
        default_factory=list)  # unit/channel filters


# ---------------------------------------------------------------------------
# MapParameters
# ---------------------------------------------------------------------------

@dataclass
class MapParameters:
    """
    Parameters for one cross-validated spatial / tuning map analysis.

    A map is defined by a single multi-axis predictor (up to X, Y, Z) and a
    single output (neural) variable.  The analysis computes cross-validated
    rate maps, optional shuffle controls, and optional tuning statistics.

    Predictor and output
    --------------------
    predictor : PredictorParameters
        Defines the stimulus / behavioral variable(s) to map (X, Y, Z axes).
        Leave Y / Z axes at their defaults ('none') for 1D or 2D maps.
    output : OutputParameters
        Defines the neural response variable (e.g. spike train) and any
        unit-selection subset conditions.

    Temporal smoothing
    ------------------
    Tsmthwin : float
        Causal smoothing window applied to the raw response signal before
        binning, in seconds.  0.0 = no smoothing.

    Occupancy thresholds
    --------------------
    OccThresh : float
        Minimum time the animal must spend in a bin (seconds) for that bin
        to be included.  Bins below threshold are masked as NaN.
    OccTrialThresh : int
        Minimum number of trials visiting a bin for that bin to be included.
        0 = no trial-count threshold.

    Output type
    -----------
    Fratemap : bool
        True  → express map in firing rate (Hz = spikes / occupancy time).
        False → express map as raw spike count per bin.

    Shuffle controls
    ----------------
    shuffle : dict
        nShf      (int)  : number of shuffle iterations; 0 = disabled.
        shftype   (str)  : 'random shift' (circular time shift) or
                           'random perm' (random permutation).
        FshfZvsXY (bool) : True to permute only the Z axis (keeping X/Y
                           intact), useful for testing Z-specific tuning.

    Cross-validation
    ----------------
    crossvalidation : dict
        kfold        (int)  : number of CV folds (e.g. 20).
        Fbestmodel   (bool) : True = use the single best-fold model;
                              False = use the full-data model.
        Fdiscarditer (bool) : True to discard per-fold tuning curves after
                              averaging (saves memory).
        Fdiscardpred (bool) : True to discard per-sample predictions after
                              scoring (saves memory).

    Data subsetting
    ---------------
    subsetInfo : list[list]
        Conditions applied to behavioral / trial data before computing the
        map.  Each entry: [origin, field, value, operator, split_by_value].
        split_by_value=True produces a separate map per unique value.
        Example: [['Beh', 'gain', [0.4, 0.6], '=', True]] → one map per gain.

    Analysis functions
    ------------------
    fun_cvmaps : str
        Name of the function that computes the cross-validated maps.
    fun_tuningstats : str
        Name of the function that computes tuning statistics from the maps.
    """

    name: str = "MAP#1"

    # Predictor and output — use field(default_factory=…) to avoid the shared-
    # mutable-default pitfall with dataclass instances.
    predictor: PredictorParameters = field(default_factory=PredictorParameters)
    output: OutputParameters = field(default_factory=OutputParameters)

    # Temporal smoothing of the response signal (seconds)
    Tsmthwin: float = 0.0

    # Occupancy thresholds
    OccThresh: float = 0.3       # minimum occupancy per bin (s)
    OccTrialThresh: int = 0      # minimum number of trials per bin

    # Output type
    Fratemap: bool = True        # True = rate map (Hz); False = count map

    # Shuffle controls
    shuffle: dict[str, Any] = field(default_factory=lambda: {
        "nShf": 0,               # number of shuffle iterations (0 = off)
        "shftype": "random shift",  # 'random shift' | 'random perm'
        "FshfZvsXY": False,      # True = permute Z axis only
    })

    # Cross-validation
    crossvalidation: dict[str, Any] = field(default_factory=lambda: {
        "kfold": 20,             # number of CV folds
        "Fbestmodel": False,     # True = best fold; False = full-data model
        "Fdiscarditer": True,    # discard per-fold curves to save memory
        "Fdiscardpred": True,    # discard per-sample predictions to save memory
    })

    # Data subset conditions [origin, field, value, operator, split_by_value]
    subsetInfo: list[list[Any]] = field(default_factory=list)

    # Analysis function names
    fun_cvmaps: str = "ComputeCVMaps"
    fun_tuningstats: str = "getTuningStats"


# ---------------------------------------------------------------------------
# GLMParameters
# ---------------------------------------------------------------------------

@dataclass
class GLMParameters:
    """
    Parameters for one Generalized Linear Model (GLM) analysis.

    A GLM models spike / neural activity as a function of one or more
    predictor variables.  Each predictor is represented by a
    PredictorParameters instance; up to 10 predictors are supported.

    Model specification
    -------------------
    name : str
        Human-readable identifier for this GLM configuration.
    distribution : str
        Error distribution: 'poisson' (default, for spike counts) or
        'gaussian' (for continuous signals).
    PerfMeasure : str
        Performance metric used for model / predictor selection:
        'nLLH' (negative log-likelihood), 'BIC', 'AIC', or 'none'.
    pvalthresh : float
        P-value threshold for statistical comparison of nested models.

    Predictors and output
    ---------------------
    predictors : list[PredictorParameters]
        Ordered list of model predictors (up to 10).  Each PredictorParameters
        defines one additive term in the GLM (e.g. position, speed, direction).
        Unused entries are left at their defaults ('none').
    output : OutputParameters
        Neural response variable (e.g. spike train) and unit-selection filters.

    Output type
    -----------
    Fratemap : bool
        True → normalise predictions to firing rate (Hz).
        False → keep as raw count.

    Spike history filter
    --------------------
    spike_history : dict
        Fhistory        (bool)        : include a spike-history filter.
        historyRange    (list[float]) : [t_min, t_max] delays for the history
                                        filter (seconds).
        historyStep     (float)       : step size for history delays (s).
        historysmthNbins (int)        : smoothing of the history kernel (bins).

    General parameters
    ------------------
    Fintercept : bool
        True to include an intercept (baseline firing rate) term.
    Tsmthwin : float
        Causal smoothing window on the response signal (seconds).
    OccThresh : float
        Minimum occupancy per bin (seconds); under-sampled bins are excluded.
    OccTrialThresh : int
        Minimum number of trials per bin.

    Shuffle and cross-validation
    ----------------------------
    shuffle : dict
        nShf    (int) : shuffle iterations; 0 = disabled.
        shftype (str) : 'random shift' | 'random perm'.
    crossvalidation : dict
        kfold      (int)  : number of CV folds.
        Fbestmodel (bool) : True = use best-fold model.

    Regularization (elastic net)
    ----------------------------
    regularization : dict
        nlambda (int)   : number of λ values to search; 0 = no regularisation.
        alpha   (float) : elastic-net mixing: 0.0 = ridge, 1.0 = lasso.
    maxit : int
        Maximum coordinate-descent iterations.
    thresh : float
        Convergence tolerance (change in log-likelihood).
    Fstandardize : bool
        True to z-score each predictor before fitting.

    Output control
    --------------
    discard_iter : bool
        True to discard per-fold model objects after averaging.
    discard_pred : bool
        True to discard per-sample predictions after scoring.

    Data subsetting
    ---------------
    subsetInfo : list[list]
        Trial / behavioral filter conditions (same format as MapParameters).

    Analysis functions
    ------------------
    fun_glms : str
        Name of the function that fits the GLMs.
    fun_tuningstats : str
        Name of the function that computes tuning statistics.
    """

    name: str = "GLM#1"

    # Model type
    distribution: str = "poisson"   # 'poisson' | 'gaussian'
    PerfMeasure: str = "nLLH"        # 'nLLH' | 'BIC' | 'AIC' | 'none'
    pvalthresh: float = 0.05         # p-value threshold for model comparison

    # Predictors (up to 10 additive model terms)
    predictors: list[PredictorParameters] = field(
        default_factory=lambda: [PredictorParameters() for _ in range(10)]
    )

    # Output / response variable
    output: OutputParameters = field(default_factory=OutputParameters)

    # Output type
    Fratemap: bool = True            # True = rate (Hz); False = count

    # Spike history filter
    spike_history: dict[str, Any] = field(default_factory=lambda: {
        "Fhistory": False,           # include spike-history filter
        "historyRange": [0.01, 0.1],  # [t_min, t_max] for history delays (s)
        "historyStep": 0.01,         # step size for history delays (s)
        "historysmthNbins": 1,       # smoothing of history kernel (bins)
    })

    # General fitting parameters
    Fintercept: bool = True          # include intercept term
    Tsmthwin: float = 0.0            # response smoothing window (s)
    OccThresh: float = 0.3           # minimum occupancy per bin (s)
    OccTrialThresh: int = 1          # minimum trials per bin

    # Shuffle and cross-validation
    shuffle: dict[str, Any] = field(default_factory=lambda: {
        "nShf": 0,                   # shuffle iterations (0 = off)
        "shftype": "random shift",   # 'random shift' | 'random perm'
    })
    crossvalidation: dict[str, Any] = field(default_factory=lambda: {
        "kfold": 10,                 # number of CV folds
        "Fbestmodel": False,         # True = use best-fold model
    })

    # Regularization (elastic net)
    regularization: dict[str, Any] = field(default_factory=lambda: {
        "nlambda": 0,                # lambda grid size (0 = no regularisation)
        "alpha": 1.0,                # mixing: 0 = ridge, 1 = lasso
    })
    maxit: int = 10000               # max coordinate-descent iterations
    thresh: float = 0.001            # convergence tolerance
    Fstandardize: bool = True        # z-score predictors before fitting

    # Output control
    discard_iter: bool = True        # discard per-fold models after averaging
    discard_pred: bool = True        # discard per-sample predictions after scoring

    # Data subset conditions
    subsetInfo: list[list[Any]] = field(default_factory=list)

    # Analysis function names
    fun_glms: str = "RunGLMs"
    fun_tuningstats: str = "getTuningStats"


# ---------------------------------------------------------------------------
# DecoderParameters
# ---------------------------------------------------------------------------

@dataclass
class DecoderParameters:
    """
    Parameters for one decoding analysis.

    A decoder predicts one or more behavioral / task variables from neural
    activity.  Up to 10 variables can be decoded simultaneously; each is
    described by a PredictorParameters entry in the predictors list.  The
    neural signal used as the predictor is described by OutputParameters
    (reusing the same container for symmetry with the other analyses).

    Decoder type
    ------------
    name : str
        Human-readable identifier for this decoder configuration.
    type : str
        Algorithm: 'Bayes' (Bayesian population vector), 'Linear'
        (linear regression / discriminant), or 'ANN' (neural network).

    Decoded variables and neural predictor
    ----------------------------------------
    predictors : list[PredictorParameters]
        Each entry defines one variable to decode (X/Y axes = the variable's
        discretisation).  Up to 10 simultaneous decoded variables.  Unused
        entries are left at their defaults ('none').
    output : OutputParameters
        The neural signal used as predictor input (e.g. population spike
        trains) and any unit-selection filters.

    Time windows
    ------------
    Tdecwin : float
        Decoding window duration (milliseconds).  Neural activity within each
        window is integrated before decoding.
    Tmemorywin : float
        Memory window (ms): how far back to integrate activity for temporal
        context.  0.0 = no memory.
    Tsmthwin : float
        Temporal smoothing applied to the decoded signal (ms).

    Occupancy thresholds
    --------------------
    OccThresh : float
        Minimum occupancy per position bin (seconds) required to include a
        bin in the encoding model.
    OccTrialThresh : int
        Minimum number of trials per bin.

    Decoder options
    ---------------
    FalwaysGLM : bool
        True to always build the encoding model using a full GLM (rather than
        a simple rate map).
    PerfMeasure : str
        Metric for encoding-model selection: 'nlogL', 'BIC', etc.
    FKOdecoding : bool
        True to run knock-out decoding: iteratively remove each predictor
        unit to estimate its contribution to decoding accuracy.
    FuniformPrior : bool
        True to use a uniform spatial prior (flat prior over all positions).
        False to use an empirical prior (proportional to occupancy).

    Cross-validation
    ----------------
    crossvalidation : dict
        kfold      (int)  : number of CV folds for the encoding model.
        Fbestmodel (bool) : True = use best-fold encoding model.

    Data subsets
    ------------
    TrainingSubsetInfo : list[list]
        Conditions applied to select the training data subset.
        Format: [origin, field, value, operator, split_by_value].
    PredictorSubsetInfo : list[list]
        Conditions applied to select which units / channels are used as
        neural predictors.  Format: [origin, field, value, operator,
        split_by_value].
    """

    name: str = "Decoder#1"

    # Algorithm
    type: str = "Bayes"              # 'Bayes' | 'Linear' | 'ANN'

    # Decoded variables (up to 10) and neural predictor
    predictors: list[PredictorParameters] = field(
        default_factory=lambda: [PredictorParameters() for _ in range(10)]
    )
    output: OutputParameters = field(default_factory=OutputParameters)

    # Time windows (milliseconds)
    Tdecwin: float = 250.0           # decoding window duration (ms)
    Tmemorywin: float = 0.0          # memory / history window (ms)
    Tsmthwin: float = 0.0            # decoded-signal smoothing (ms)

    # Occupancy thresholds
    OccThresh: float = 0.3           # minimum bin occupancy (s)
    OccTrialThresh: int = 0          # minimum trials per bin

    # Decoder options
    FalwaysGLM: bool = True          # always use GLM encoding model
    PerfMeasure: str = "nLLH"        # encoding-model selection metric
    FKOdecoding: bool = True         # run knock-out contribution analysis
    FuniformPrior: bool = True       # True = flat prior; False = empirical

    # Cross-validation of the encoding model
    crossvalidation: dict[str, Any] = field(default_factory=lambda: {
        "kfold": 10,                 # number of CV folds
        "Fbestmodel": False,         # True = use best-fold model
    })

    # Data subset conditions
    TrainingSubsetInfo: list[list[Any]] = field(default_factory=list)
    PredictorSubsetInfo: list[list[Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# CustomParameters
# ---------------------------------------------------------------------------

@dataclass
class CustomParameters:
    """
    Parameters for a user-defined analysis.

    Allows arbitrary Python functions to be invoked with a named parameter
    dictionary, following the same subset-condition convention as the built-in
    analyses.

    Attributes
    ----------
    name : str
        Human-readable identifier for this custom analysis.
    functionName : str
        Name of the Python function to call.  Must be importable at runtime.
    functionParams : dict
        Keyword arguments passed directly to the function.
    subsetInfo : list[list]
        Data subset conditions applied before calling the function.
        Format: [origin, field, value, operator, split_by_value].
    """

    name: str = "Custom#1"
    functionName: str = ""                                       # callable name
    functionParams: dict[str, Any] = field(
        default_factory=dict)  # kwargs for the function
    subsetInfo: list[list[Any]] = field(default_factory=list)    # data filters

from dataclasses import dataclass, field


@dataclass
class LoadParameters:
    """
    Parameters for loading experimental data

    Attributes:
        project_dir: Root directory where experimental data is stored
        path_explorer: Name of function to use for navigating directory structure
        subsetInfo: Dictionary specifying what subset of data to load
            - load_all: Whether to load all available data
            - trial_range: [start, end] trial indices or None for all
            - cell_ids: List of specific cell IDs or None for all
            - time_range: [start, end] time range in seconds or None
        sync_signal: Type of synchronization signal (e.g., 'ttl' or 'behavior')
        animal: Animal identifier (set by user/GUI)
        series: Recording series identifier (set by user/GUI)
        exp: Experiment identifier (set by user/GUI)
    """
    project_dir: str = ""
    path_explorer: str = "default_path_explorer"
    subsetInfo: dict = field(default_factory=dict)
    sync_signal: str = "behavior"
    animal: str = ""
    series: str = ""
    exp: str = ""

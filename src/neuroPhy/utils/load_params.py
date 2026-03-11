from pathlib import Path
from typing import Any

import yaml

import config


def default_params() -> dict[str, Any]:
    """
    Load default parameters for all analysis types

    These defaults can be overridden by the user's params.yaml file.

    Returns:
        Dictionary with default parameters organized by analysis type
    """
    defaults = {
        'load': {
            'project_dir': str(Path.home()),
            'path_explorer': 'default_path_explorer',
            'subsetInfo': {
                'load_all': True,
                'trial_range': None,
                'cell_ids': None,
                'time_range': None,
            },
            'sync_signal': 'ttl',
        },
        'map': {
            'name': 'Map#1',
            'varXorigin': 'Beh',
            'varYorigin': 'Beh',
            'varZorigin': 'none',
            'varOorigin': 'Spk',
            'varXname': 'XPercent',
            'varYname': 'YPercent',
            'varZname': 'none',
            'varOname': 'spikeTrain',
            'Tsmthwin': 0.0,
            'OccThresh': 0.3,
            'OccTrialThresh': 0,
            'Xbinsize': 1.0,
            'XsmthNbins': 1,
            'Xrange': [0.0, 100.0],
            'Xbinedges': list(range(0, 101)),
            'FclampX': False,
            'FcircularX': False,
            'Ybinsize': 1.0,
            'YsmthNbins': 4,
            'Yrange': [0.0, 100.0],
            'Ybinedges': list(range(0, 101)),
            'FclampY': False,
            'FcircularY': False,
            'Zbinsize': None,
            'ZsmthNbins': None,
            'Zrange': None,
            'Zbinedges': None,
            'FclampZ': False,
            'FcircularZ': False,
            'Fratemap': True,
            'nShf': 0,
            'shftype': 'random shift',
            'FshfZvsXY': False,
            'kfold': 20,
            'Fbestmodel': False,
            'Fdiscarditer': True,
            'Fdiscardpred': True,
            'subsetInfo': [
                ['Beh', 'contrast', [0, 1], '=', False],
                ['Beh', 'outcome', 2, '=', False],
                ['Beh', 'smthRunSpeed', 2.5, '>', False],
                ['Beh', 'blanks', 0, '=', False],
                ['Beh', 'gain', [0.4, 0.5, 0.6], '=', True],
                ['none', 'none', None, '=', False],
            ],
            'outputsubsetInfo': [['none', 'none', None, '=']],
            'fun_cvmaps': 'ComputeCVMaps',
            'fun_tuningstats': 'getTuningStats',
        },
        'glm': {
            'name': 'GLM#1',
            'distribution': 'poisson',
            'PerfMeasure': 'nLLH',
            'pvalthresh': 0.05,
            'Flinear': [False] * 10,
            'TimeRange': [0] * 10,
            'TimeStep': [0] * 10,
            'TsmthNbins': [0] * 10,
            'varXorigin': ['Nav'] + ['none'] * 9,
            'varYorigin': ['Nav'] + ['none'] * 9,
            'varZorigin': ['none'] * 10,
            'varXname': ['XPercent'] + ['none'] * 9,
            'varYname': ['YPercent'] + ['none'] * 9,
            'varZname': ['none'] * 10,
            'Xbinsize': [5] + [None] * 9,
            'XsmthNbins': [1] + [None] * 9,
            'Xrange': [[0, 100]] + [None] * 9,
            'Xbinedges': [list(range(0, 101))] + [None] * 9,
            'FcircularX': [False] * 10,
            'FclampX': [False] * 10,
            'Ybinsize': [5] + [None] * 9,
            'YsmthNbins': [1] + [None] * 9,
            'Yrange': [[0, 100]] + [None] * 9,
            'Ybinedges': [list(range(0, 101))] + [None] * 9,
            'FcircularY': [False] * 10,
            'FclampY': [False] * 10,
            'Zbinsize': [None] * 10,
            'ZsmthNbins': [None] * 10,
            'Zrange': [None] * 10,
            'Zbinedges': [None] * 10,
            'FcircularZ': [False] * 10,
            'FclampZ': [False] * 10,
            'Fratemap': True,
            'FalwaysIn': [False] * 10,
            'Fremovenan': [False] * 10,
            'varOorigin': 'Spk',
            'varOname': 'spikeTrain',
            'Fhistory': False,
            'historyRange': [0.01, 0.1],
            'historyStep': 0.01,
            'historysmthNbins': 1,
            'Fintercept': True,
            'Tsmthwin': 0.0,
            'OccThresh': 0.3,
            'OccTrialThresh': 1,
            'nShf': 0,
            'shftype': 'random shift',
            'kfold': 10,
            'nlambda': 0,
            'maxit': 10000,
            'thresh': 0.001,
            'alpha': 1.0,
            'Fstandardize': True,
            'Fdiscarditer': True,
            'Fdiscardpred': True,
            'subsetInfo': [
                ['Beh', 'contrast', [0, 1], '=', False],
                ['Beh', 'outcome', 2, '=', False],
                ['Beh', 'smthRunSpeed', 5, '>', False],
                ['Beh', 'blanks', 0, '=', False],
                ['Beh', 'gain', 1, '=', True],
                ['Beh', 'none', None, '=', False],
            ],
            'outputsubsetInfo': [['Spk', 'Probe', 1, '=']],
            'fun_glms': 'RunGLMs',
            'fun_tuningstats': 'getTuningStats',
        },
    }
    return defaults


def params_from_saved(filepath: str) -> dict[str, Any]:
    """
    Load parameters from a YAML file

    Args:
        filepath: Path to YAML file

    Returns:
        Dictionary with parameters
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Parameters file not found: {filepath}")

    with open(filepath) as f:
        params = yaml.safe_load(f)

    return params


def merge_params(defaults: dict[str, Any], user_params: dict[str, Any]) -> dict[str, Any]:
    """
    Merge user parameters with defaults

    User parameters override defaults.

    Args:
        defaults: Default parameters
        user_params: User-provided parameters

    Returns:
        Merged parameters dictionary
    """
    merged = defaults.copy()

    for key, value in user_params.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            # Recursively merge nested dictionaries
            merged[key] = merge_params(merged[key], value)
        else:
            merged[key] = value

    return merged

"""
scenfirepy

Python implementation of the SCENFIRE fire-scenario framework.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("scenfirepy")
except PackageNotFoundError:
    __version__ = "0.0.0"

from .preprocess import check_fire_data
from .distribution import build_target_hist, calculate_discrepancy, fit_powerlaw
from .selection import select_events
from .params import get_select_params
from .create_distribution import create_distribution
from .burn_probability import calc_burn_probability
from .flp20_to_df import flp20_to_df
from .flp20_to_bp_df import flp20_to_bp_df
from .flp20_to_raster import flp20_to_raster

__all__ = [
    "check_fire_data",
    "build_target_hist",
    "calculate_discrepancy",
    "fit_powerlaw",
    "select_events",
    "get_select_params",
    "create_distribution",
    "calc_burn_probability",
    "flp20_to_df",
    "flp20_to_bp_df",
    "flp20_to_raster",
]

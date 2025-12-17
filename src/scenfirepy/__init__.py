"""
scenfirepy

Python implementation of the SCENFIRE fire-scenario framework.
"""

__version__ = "0.1.0"

from .preprocess import check_fire_data
from .distribution import build_target_hist, calculate_discrepancy
from .selection import select_events
from .params import get_select_params

from .create_distribution import create_distribution
from .burn_probability import calc_burn_probability
from .flp20_to_df import flp20_to_df
from .flp20_to_bp_df import flp20_to_bp_df
from .flp20_to_raster import flp20_to_raster

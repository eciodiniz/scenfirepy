"""
scenfirepy

Python implementation of the SCENFIRE fire-scenario framework.
"""

__version__ = "0.1.0"

# Core distribution logic
from .distribution import (
    build_target_hist,
    calculate_discrepancy,
    fit_powerlaw
)

# Scenario creation
from .create_distribution import create_distribution

# Event selection
from .selection import select_events

# Burn probability
from .burn_probability import calc_burn_probability

# FLP20 converters
from .flp20_to_df import flp20_to_df
from .flp20_to_bp_df import flp20_to_bp_df
from .flp20_to_raster import flp20_to_raster

# Parameters / validation
from .params import get_select_params
from .preprocess import check_fire_data

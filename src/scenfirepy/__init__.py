"""
scenfirepy

Python implementation of the SCENFIRE fire-scenario framework.
(R-parity port)
"""

__version__ = "0.1.0"

# Core validation / preprocessing
from .preprocess import check_fire_data

# Parameter handling
from .params import get_select_params

# Distribution & discrepancy
from .distribution import (
    build_target_hist,
    calculate_discrepancy,
    fit_powerlaw,
)

# Event selection & orchestration
from .selection import select_events
from .create_distribution import create_distribution

# Burn probability
from .burn_probability import calc_burn_probability

# FLP20 converters
from .flp20_to_df import flp20_to_df
from .flp20_to_bp_df import flp20_to_bp_df
from .flp20_to_raster import flp20_to_raster

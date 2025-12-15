"""
scenfirepy

Python implementation of the SCENFIRE fire-scenario framework.
"""

__version__ = "0.1.0"

from .io import read_flp20_csv
from .preprocess import validate_fire_dataframe, compute_fire_size
from .distribution import fit_powerlaw_distribution, build_target_histogram
from .selection import calculate_discrepancy, select_events
from .spatial import validate_geodataframe
from .raster import rasterize_geometries
from .viz import plot_fire_size_distribution

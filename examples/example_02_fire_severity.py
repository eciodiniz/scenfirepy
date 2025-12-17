"""
Example 2 — Fire severity–based scenario selection

This example applies scenfirepy to a raster of fire severity derived from
satellite imagery. Each raster cell represents how strongly vegetation
was affected by a real wildfire, and is interpreted as a potential fire
event magnitude. The algorithm selects a subset of events whose size
distribution reproduces the observed severity-based fire regime.
"""

import scenfirepy
import numpy as np
import pandas as pd
import rasterio

# ------------------------------------------------------
# 1. LOAD FIRE SEVERITY RASTER (LOCAL GeoTIFF)
# ------------------------------------------------------
# The raster contains spatially explicit burn severity values.
# Only strictly positive values are meaningful for SCENFIRE.

raster_path = r"D:\AXA-Chile\Simulations\SCENFIRE-main\Severity_CL-VS_ID190189_u460_20180313.tif"

with rasterio.open(raster_path) as src:
    severity = src.read(1).astype(float)

severity[severity <= 0] = np.nan


# ------------------------------------------------------
# 2. CONVERT RASTER → EVENT VECTORS
# ------------------------------------------------------
# Each valid raster cell is treated as a candidate fire event.

# Fire-event magnitudes (burn severity)
sizes = severity[np.isfinite(severity)]

# Exposure weights (uniform when no spatial weighting is available)
event_surfaces = np.ones_like(sizes)


# ------------------------------------------------------
# 3. CREATE DISTRIBUTION (SCENFIRE CORE ALGORITHM)
# ------------------------------------------------------
# Selects a subset of events whose size distribution best matches
# a target power-law fire regime.

result = scenfirepy.create_distribution(
    sizes=sizes,
    event_surfaces=np.ones_like(sizes) + 1e-6 * np.arange(sizes.size),
    xmin=np.nanpercentile(sizes[sizes > 0], 5),
    alpha=2.3,
    num_bins=10,
    seed=123
)


# ------------------------------------------------------
# 4. USER-FACING OUTPUT
# ------------------------------------------------------
# Selected event magnitudes and discrepancy metric.

df = pd.DataFrame({
    "selected_event_size": result["events"]
})

print("Discrepancy:", result["discrepancy"])
print(df.head())

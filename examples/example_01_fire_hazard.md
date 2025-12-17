# EXAMPLE 1 — Fire hazard–based scenario selection

This example demonstrates how **scenfirepy** can be used to select a subset of candidate fire events whose size distribution reproduces a historical fire regime derived from **raster-based fire hazard data**. 

The fire hazard raster used here is distributed with the R package **fireexposuR** and is openly available at: https://github.com/ropensci/fireexposuR


---

## Overview

The workflow follows four conceptual steps:

1. Load a fire hazard raster (GeoTIFF)
2. Convert raster values into event vectors
3. Apply the SCENFIRE selection algorithm
4. Inspect the selected fire-size scenario


---

## Code example

```python
import scenfirepy
import numpy as np
import pandas as pd
import rasterio

# ------------------------------------------------------
# 1. LOAD FIRE HAZARD RASTER
# ------------------------------------------------------
# We use a small, open-access fire hazard raster distributed with the R package
# fireexposuR. This raster represents spatial variation in fire hazard intensity
# and is used here as a proxy for a historical fire regime.

url = (
    "https://raw.githubusercontent.com/ropensci/fireexposuR/"
    "master/inst/extdata/hazard.tif"
)

with rasterio.open(url) as src:
    hazard = src.read(1).astype(float)

# The SCENFIRE logic assumes strictly positive event magnitudes.
# Non-positive or invalid pixels are removed.
hazard[hazard <= 0] = np.nan


# ------------------------------------------------------
# 2. CONVERT RASTER → EVENT VECTORS
# ------------------------------------------------------
# Raster cells are interpreted as potential fire events.

# Fire "sizes" correspond to hazard intensity values
sizes = hazard[np.isfinite(hazard)]

# Event surfaces represent exposure or area weights.
# When no spatial weighting is available, a uniform surface is used.
event_surfaces = np.ones_like(sizes)


# ------------------------------------------------------
# 3. CREATE DISTRIBUTION (SCENFIRE CORE ALGORITHM)
# ------------------------------------------------------
# This step constructs a target fire-size distribution and selects
# a subset of events whose distribution best matches that target.

result = scenfirepy.create_distribution(
    sizes=sizes,

    # A small deterministic jitter avoids numerical degeneracy when
    # event surfaces are otherwise identical.
    event_surfaces=np.ones_like(sizes) + 1e-6 * np.arange(sizes.size),

    # Lower cutoff for the distribution.
    # A low percentile removes noise-dominated small values.
    xmin=np.nanpercentile(sizes[sizes > 0], 5),

    # Power-law exponent controlling the target distribution shape
    alpha=2.3,

    # Histogram resolution kept modest for numerical stability
    num_bins=10,

    # Seed ensures reproducibility
    seed=123
)


# ------------------------------------------------------
# 4. USER-FACING OUTPUT
# ------------------------------------------------------
# The output includes:
# - selected fire event sizes
# - a discrepancy metric measuring the match to the target distribution

df = pd.DataFrame({
    "selected_event_size": result["events"]
})

print("Discrepancy:", result["discrepancy"])
print(df.head())

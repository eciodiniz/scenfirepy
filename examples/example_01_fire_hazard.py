"""
EXAMPLE 1 — Fire hazard–based scenario selection

This example demonstrates how scenfirepy can bwe used to select
a subset of simulated fire events whose size distribution reproduces a
historical fire regime derived from raster-based fire hazard data from
R package "fireexposuR", available at: https://github.com/ropensci/fireexposuR

"""

import scenfirepy
import numpy as np
import pandas as pd
import rasterio

# ------------------------------------------------------
# 1. LOAD FIRE HAZARD RASTER 
# ------------------------------------------------------
# We use a small, open-access fire hazard raster distributed with the R package
# fireexposuR. This raster represents spatial variation in fire hazard intensity
# and serves here as a proxy for a historical fire regime.

url = (
    "https://raw.githubusercontent.com/ropensci/fireexposuR/"
    "master/inst/extdata/hazard.tif"
)

with rasterio.open(url) as src:
    hazard = src.read(1).astype(float)

# The package logic assumes strictly positive event magnitudes.
# Non-positive or invalid pixels are removed.
hazard[hazard <= 0] = np.nan


# ------------------------------------------------------
# 2. CONVERT RASTER → EVENT VECTORS 
# ------------------------------------------------------
# Fire events are represented as vectors rather than rasters.
# Each raster cell is interpreted as a potential fire event.

# "sizes" correspond to fire magnitudes (here: hazard intensity values)

sizes = hazard[np.isfinite(hazard)]

# "event_surfaces" represent exposure or area weights associated with each event.
# When no spatial weighting is available, a uniform surface is used.

event_surfaces = np.ones_like(sizes)


# ------------------------------------------------------
# 3. CREATE DISTRIBUTION (SCENFIRE CORE ALGORITHM)
# ------------------------------------------------------
# This is the central step:
# - a target fire-size distribution is constructed
# - simulated events are iteratively selected
# - the selected subset best matches the target distribution

result = scenfirepy.create_distribution(
    sizes=sizes,

    # A tiny deterministic jitter avoids numerical degeneracy when surfaces are uniform,
    # without altering the conceptual meaning of equal exposure.
    event_surfaces=np.ones_like(sizes) + 1e-6 * np.arange(sizes.size),

    # xmin defines the lower cutoff of the distribution.
    # Using a low percentile removes noise-dominated small values,
    # following common practice in fire-size distribution analysis.
    xmin=np.nanpercentile(sizes[sizes > 0], 5),

    # Power-law exponent controlling the target distribution shape
    alpha=2.3,

    # Histogram resolution kept modest for numerical stability
    num_bins=10,

    # Seed ensures full reproducibility of the stochastic selection
    seed=123
)


# ------------------------------------------------------
# 4. USER-FACING OUTPUT
# ------------------------------------------------------
# The output consists of:
# - the selected fire event sizes
# - a discrepancy metric quantifying the match to the target distribution

df = pd.DataFrame({
    "selected_event_size": result["events"]
})

print("Discrepancy:", result["discrepancy"])
print(df.head())


# This step applies the SCENFIRE core algorithm: it selects a subset of fire events
# whose size distribution best matches a target power-law distribution.
# - sizes: fire intensity / magnitude extracted from the raster
# - event_surfaces: exposure weights (kept nearly uniform, small jitter avoids degeneracy)
# - xmin: lower cutoff (robustly set from lower tail to exclude noise/small artifacts)
# - alpha: power-law exponent controlling the target distribution shape
# - num_bins: histogram resolution (kept low for numerical stability)
# - seed: ensures reproducibility

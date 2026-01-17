# EXAMPLE 1 — Fire hazard–based scenario selection

This example demonstrates how **scenfirepy** can be used to select a subset of candidate fire events whose size distribution reproduces a historical fire regime derived from **raster-based fire hazard data**. 
In short, the scenfirepy selection algorithm to raster-derived fire hazard data. Each raster cell is treated as a candidate fire event,
and the algorithm selects a subset of events whose size distribution best reproduces a target power-law fire regime.
The resulting scenario can be used for downstream analyses such as burn probability estimation, scenario comparison, or risk assessment.

The fire hazard raster used here is distributed with the R package **fireexposuR** and is openly available at: https://github.com/ropensci/fireexposuR
``

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
import numpy as np
import rasterio
from pathlib import Path
from scenfirepy import build_target_hist, select_events
from scenfirepy.burn_probability import calc_burn_probability

# ------------------------------------------------------
# USER INPUTS AND CONTROLS
# ------------------------------------------------------
SRC = (
    "https://raw.githubusercontent.com/ropensci/fireexposuR/"
    "master/inst/extdata/hazard.tif"
) # Input raster of observed fire hazard
OUT_TIF = r"D:\AXA-Chile\Simulations\SCENFIRE-main\hazard_bp.tif"    # Output raster: scenario-based hazard probability
SEED = 123                            # Random seed for reproducible selection
SURF_FRAC = 0.40  

# SRC is an empirical fire-hazard raster where each pixel quantifies burn hazard. 
# OUT_TIF will store the spatial representation of the selected scenario.
# SURF_FRAC controls the *scale* of the scenario: smaller values represent rarer,
# more extreme scenarios; larger values represent more extensive ones.

# ------------------------------------------------------
# 1) LOAD hazard RASTER AND PRESERVE SPATIAL GRID
# ------------------------------------------------------
with rasterio.open(SRC) as src:
    data = src.read(1).astype(float)
    profile = src.profile.copy() 

# The raster profile (CRS, resolution, extent) defines the spatial framework in which scenfirepy outputs will stay.  
# Preserving it ensures that the final GeoTIFF aligns exactly with the input hazard data and with any other spatial 
# layers used by the analyst (e.g., assets, vegetation, administrative boundaries).


# ------------------------------------------------------
# 2) CONVERT RASTER CELLS INTO EVENT VECTORS
# ------------------------------------------------------
mask = np.isfinite(data) & (data > 0)
sizes = data[mask]

# Event surfaces represent the spatial weight of each event. Here, each pixel is assumed to contribute equally, so a 
# uniform surface is used. A tiny deterministic jitter is added only to avoid numerical degeneracy when all surfaces
# are identical. event_surfaces = np.ones_like(sizes) + 1e-6 * np.arange(sizes.size)

# In scenfirepy, each candidate fire event is represented by two vectors:
#   - `sizes`: the event magnitude (here, hazard value of each pixel)
#   - `event_surfaces`: the spatial weight or exposure associated with that event
# This abstraction allows the selection algorithm to operate independently of
# spatial geometry, while still preserving spatial meaning through later mapping.

# ------------------------------------------------------
# 3) CONSTRUCT TARGET DISTRIBUTION (HISTOGRAM)
# ------------------------------------------------------
tinfo = build_target_hist(
    sizes=sizes,
    event_surfaces=event_surfaces,
    num_bins=10
)
target_hist = tinfo["target_hist"]
bins = tinfo["bins"]

# The target histogram summarizes the empirical distribution of hazard values. The selection algorithm does not try
# to reproduce individual pixels, but instead seeks a subset of events whose *distributional shape* (across bins)
# matches this target. This is what guarantees statistical consistency between the selected scenario and the observed
# hazard regime.

# ------------------------------------------------------
# 4) DEFINE REFERENCE SURFACE AND SCENARIO THRESHOLD
# ------------------------------------------------------
reference_surface2 = float(sizes.sum())
surface_threshold2 = reference_surface2 * SURF_FRAC

# The reference_surface here is the total observed magnitude used as a scaling reference. The surface threshold
# defines how much of that total the scenario should. In hazard examples this is the sum of hazard values (not
# physical hectares). contain. Selection stops once the accumulated selected hazard reaches this threshold,
# ensuring that scenario size is controlled explicitly and transparently. When defining your reference surface,
# choose this deliberately — for area-based scenarios use real area units instead.

# ------------------------------------------------------
# 5) RUN SCENFIREPY SELECTION ALGORITHM
# ------------------------------------------------------
res = select_events(
    event_sizes=sizes,
    event_probabilities=sizes,
    target_hist=target_hist,
    bins=bins,
    reference_surface=reference_surface2,
    surface_threshold=surface_threshold2,
    tolerance=0.1,
    iter_limit=500_000,
    max_it=200,
    seed=SEED,
)

# The algorithm repeatedly samples events without replacement, renormalizing probabilities after each draw, until
# the surface threshold is reached. Each trial is evaluated using an L1 discrepancy metric comparing the selected
# histogram to the target histogram. The trial with the smallest discrepancy is kept.

# ------------------------------------------------------
# 6) COMPUTE EVENT-LEVEL PROBABILITY WEIGHTS
# ------------------------------------------------------
sel_idx = res["surface_index"]
selected_vec = np.zeros_like(sizes, dtype=float)
selected_vec[sel_idx] = 1.0

bp_per_event = calc_burn_probability(selected_vec, event_surfaces)

# `selected_vec` is an indicator of which candidate events belong to the scenario. Thus, selected_vec is an
# index/indicator vector 
# (1 = chosen event).
# bp_per_event is scenario-relative mass assigned to selected events (it is not an absolute annual probability
# unless normalized against a physical reference surface)
# `calc_burn_probability` distributes probability mass across selected events.
# The result is a *scenario-relative probability*, not an unconditional forecast.
# In this example it answers: “given this scenario, where does hazard concentrate spatially?”

# ------------------------------------------------------
# 7) MAP EVENT PROBABILITIES BACK TO SPATIAL GRID
# ------------------------------------------------------
out = np.zeros_like(data, dtype=float)
out[mask] = bp_per_event

# Until now, all computations occurred in vector space. This step reconnects the selected scenario to geographic 
# space, producing a raster where each pixel value reflects its contribution to the selected scenario.

# ------------------------------------------------------
# 8) EXPORT FINAL GEO-TIFF
# ------------------------------------------------------
profile.update(dtype="float32", count=1, nodata=0.0)
Path("Final").mkdir(parents=True, exist_ok=True)

with rasterio.open(OUT_TIF, "w", **profile) as dst:
    dst.write(out.astype("float32"), 1)

# The exported GeoTIFF is the main user-facing product of this workflow. In this example, it represents a spatially 
# explicit hazard scenario that is statistically consistent with the observed hazard regime. Thus, this GeoTIFF is  
# a scenario-consistent spatial weight map: in this example it highlights where the selected hazard mass concentrates
# under the chosen scenario (useful for comparative risk mapping, not for direct frequency forecasting).
#  Analysts can overlay this raster with assets, ecosystems, or administrative units to compare relative impacts, 
# prioritize interventions, or evaluate alternative scenario assumptions.

print("Done:", OUT_TIF)
print(
    "Selected events:", len(sel_idx),
    "Selected surface:", res["total_surface"],
    "Discrepancy:", res["discrepancy"]
)

# In the output performance metrics of the quality of the raster produced: 
# `Discrepancy` measures how closely the selected hazard distribution matches the target hazard regime
# (L1 distance between histograms).
# For example, discrepancy < 0.15 → acceptable match and < 0.15 → acceptable match
# `Selected events (98)` represent the raster cells (hazard “events”) retained by the algorithm.
# More selected events = more flexibility
# `Selected sufraces` = sum of the pixel magnitudes (the sizes values) for the pixels chosen by select_events.
# Not hectares unless 
# sizes are in hectares. For this hazard example it represents sum of hazard intensities.

# Alternatively, you can also run the algorithm multiple times to improve performance to obtain different results
# by running multiple seeds and retaining the best result.
# For example, below the algorithm is run 10 times to select events and will extract the best result
# (i.e., smallest discrepancy)

best = None
best_disc = np.inf

for i in range(10):
    res = select_events(
        event_sizes=sizes,
        event_probabilities=sizes,
        target_hist=target_hist,
        bins=bins,
        reference_surface=reference_surface,
        surface_threshold=surface_threshold,
        tolerance=0.1,
        iter_limit=500_000,
        max_it=200,
        seed=123 + i,          # <-- only change
    )

    if res["discrepancy"] < best_disc:
        best_disc = res["discrepancy"]
        best = res

# use `best` from here on
res = best

# After the loop where `best` is selected
res = best

print("Done: severity_bp.tif")
print("Selected events:", len(res["surface_index"]))
print("Selected surface:", res["total_surface"])
print("Discrepancy:", res["discrepancy"])

#########

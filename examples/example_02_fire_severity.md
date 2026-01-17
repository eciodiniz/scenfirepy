# Example 2 — Fire severity–based scenario selection

This example uses a raster of fire severity derived from satellite imagery, where each pixel quantifies how strongly vegetation was affected by a real
wildfire event. The raster is then used to apply **scenfirepy** and select event magnitudes whose distribution reproduces the observed severity-based fire regime.

The raster used in the example below comes from the historical burned area and fire severity in Chile database by Miranda et al. (2022: https://doi.org/10.1594/PANGAEA.941127) and is related to their article from the same year (https://doi.org/10.5194/essd-14-3599-2022).

You can obtain and test the raster used as an example below from the original repository cited above, or download it here:
https://raw.githubusercontent.com/eciodiniz/scenfirepy/main/examples/Severity_CL-VS_ID190189_u460_20180313.tif

```python
import numpy as np
import rasterio
from pathlib import Path
from scenfirepy import build_target_hist, select_events
from scenfirepy.burn_probability import calc_burn_probability

# ------------------------------------------------------
# USER INPUTS AND CONTROLS
# ------------------------------------------------------
SRC = r"D:\SCENFIREPY\Files\Severity_CL-VS_ID190189_u460_20180313.tif" # Input raster of observed fire severity
OUT_TIF = "severity_bp.tif"    # Output raster: scenario-based severity probability
SEED = 123                            # Random seed for reproducible selection
SURF_FRAC = 0.40                      # Fraction of total observed severity to represent

# SRC is an empirical fire-severity raster where each pixel quantifies burn severity. 
# OUT_TIF will store the spatial representation of the selected scenario.
# SURF_FRAC controls the *scale* of the scenario: smaller values represent rarer,
# more extreme scenarios; larger values represent more extensive ones.

# ------------------------------------------------------
# 1) LOAD SEVERITY RASTER AND PRESERVE SPATIAL GRID
# ------------------------------------------------------
with rasterio.open(SRC) as src:
    data = src.read(1).astype(float)
    profile = src.profile.copy() 

# The raster profile (CRS, resolution, extent) defines the spatial framework in which scenfirepy outputs will stay. Preserving it ensures 
# that the final GeoTIFF aligns exactly with the input severity data and with any other spatial layers used by the analyst 
# (e.g., assets, vegetation, administrative boundaries).


# ------------------------------------------------------
# 2) CONVERT RASTER CELLS INTO EVENT VECTORS
# ------------------------------------------------------
mask = np.isfinite(data) & (data > 0)
sizes = data[mask]

# Event surfaces represent the spatial weight of each event. Here, each pixel is assumed to contribute equally, so a uniform surface is used.
# A tiny deterministic jitter is added only to avoid numerical degeneracy when all surfaces are identical.
event_surfaces = np.ones_like(sizes) + 1e-6 * np.arange(sizes.size)

# In scenfirepy, each candidate fire event is represented by two vectors:
#   - `sizes`: the event magnitude (here, severity value of each pixel)
#   - `event_surfaces`: the spatial weight or exposure associated with that event. In this example, these surfaces are
# *weights* per pixel (same units as sizes), not hectares.
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

# The target histogram summarizes the empirical distribution of severity values. The selection algorithm does not try to reproduce individual 
# pixels, but instead seeks a subset of events whose *distributional shape* (across bins) matches this target. This is what guarantees 
# statistical consistency between the selected scenario and the observed severity regime.

# ------------------------------------------------------
# 4) DEFINE REFERENCE SURFACE AND SCENARIO THRESHOLD
# ------------------------------------------------------
reference_surface = float(sizes.sum())
surface_threshold = reference_surface * SURF_FRAC

# The reference_surface here is the total observed magnitude used as a scaling reference. The surface threshold defines how much of that total 
# the scenario should. In severity examples this is the sum of severity values (not physical hectares). contain. Selection stops once the 
# accumulated selected severity reaches this threshold, ensuring that scenario size is controlled explicitly and transparently.
# When defining your reference surface, choose this deliberately — for area-based scenarios use real area units instead

# ------------------------------------------------------
# 5) RUN SCENFIREPY SELECTION ALGORITHM
# ------------------------------------------------------
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
    seed=SEED,
)

# The algorithm repeatedly samples events without replacement, renormalizing probabilities after each draw, until the surface threshold is 
# reached. Each trial is evaluated using an L1 discrepancy metric comparing the selected histogram to the target histogram. 
# The trial with the smallest discrepancy is kept.

# ------------------------------------------------------
# 6) COMPUTE EVENT-LEVEL PROBABILITY WEIGHTS
# ------------------------------------------------------
sel_idx = res["surface_index"]
selected_vec = np.zeros_like(sizes, dtype=float)
selected_vec[sel_idx] = 1.0

bp_per_event = calc_burn_probability(selected_vec, event_surfaces)

# `selected_vec` is an indicator of which candidate events belong to the scenario. Thus, selected_vec is an index/indicator vector 
# (1 = chosen event).
# bp_per_event is scenario-relative mass assigned to selected events (it is not an absolute annual probability unless normalized against a 
# physical reference surface)
# `calc_burn_probability` distributes probability mass across selected events. The burn_probability values are normalized according to
# calc_burn_probability semantics (per-event mass). They sum to the total selected-mass normalization used in the scenario (e.g., severity).
# The result is a *scenario-relative probability*, not an unconditional forecast.
# In this example it answers: “given this scenario, where does severity concentrate spatially?”

# ------------------------------------------------------
# 7) MAP EVENT PROBABILITIES BACK TO SPATIAL GRID
# ------------------------------------------------------
out = np.zeros_like(data, dtype=float)
out[mask] = bp_per_event

# Until now, all computations occurred in vector space. This step reconnects the selected scenario to geographic space, producing a
# raster where each pixel value reflects its contribution to the selected scenario.

# ------------------------------------------------------
# 8) EXPORT FINAL GEO-TIFF
# ------------------------------------------------------
profile.update(dtype="float32", count=1, nodata=0.0)
Path("Final").mkdir(parents=True, exist_ok=True)

with rasterio.open(OUT_TIF, "w", **profile) as dst:
    dst.write(out.astype("float32"), 1)

# The exported GeoTIFF is the main user-facing product of this workflow. In this example, it represents a spatially explicit severity 
# scenario that is statistically consistent with the observed severity regime. Thus, this GeoTIFF is a scenario-consistent spatial 
# weight map: in this example it highlights where the selected severity mass concentrates under the chosen scenario (useful for 
# comparative risk mapping, not for direct frequency forecasting).
#  Analysts can overlay this raster with assets, ecosystems, or administrative units to compare relative impacts, prioritize 
# interventions, or evaluate alternative scenario assumptions.

print("Done:", OUT_TIF)
print(
    "Selected events:", len(sel_idx),
    "Selected surface:", res["total_surface"],
    "Discrepancy:", res["discrepancy"]
)

# In the output performance metrics of the quality of the raster produced: 
# `Discrepancy` measures how closely the selected severity distribution matches the target severity regime (L1 distance between histograms).
# For example, discrepancy < 0.15 → acceptable match and < 0.15 → acceptable match
# `Selected events (98)` represent the raster cells (severity “events”) retained by the algorithm. More selected events = more flexibility
# `Selected surfaces` = sum of the pixel magnitudes (the sizes values) for the pixels chosen by select_events. Not hectares unless 
# sizes are in hectares. For severity example the selected_surface is the sum of those severity scores for the chosen pixels.

# Alternatively, you can also run the algorithm multiple times to improve performance to obtain different results by running multiple seeds and retaining the best result.
# For example, below the algorithm is run 10 times to select events and will extract the best result (i.e., smallest discrepancy)

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


###### END

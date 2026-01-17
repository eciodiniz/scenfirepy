# Example 2 — Fire severity–based scenario selection

This example uses a raster of fire severity derived from satellite imagery, where each pixel quantifies how strongly vegetation was affected by a real
wildfire event. The raster is then used to apply **scenfirepy** and select event magnitudes whose distribution reproduces the observed severity-based fire regime.

The raster used in the example below comes from the historical burned area and fire severity in Chile database by Miranda et al. (2022: https://doi.org/10.1594/PANGAEA.941127) and is related to their article from the same year (https://doi.org/10.5194/essd-14-3599-2022).

You can obtain and test the raster used as an example below from the original repository cited above, or download it here:
https://raw.githubusercontent.com/eciodiniz/scenfirepy/main/examples/Severity_CL-VS_ID190189_u460_20180313.tif

```python
import scenfirepy
import numpy as np
import pandas as pd
import rasterio

# ------------------------------------------------------
# 1. LOAD FIRE SEVERITY RASTER 
# ------------------------------------------------------
# The severity raster represents spatial variation in burn severity resulting from an observed wildfire.
# Pixel values are treated as empirical fire-event magnitudes.

raster_path = r"C:\Users\e.diniz\Downloads\scenfirepy\Severity_CL-VS_ID190189_u460_20180313.tif"

with rasterio.open(raster_path) as src:
    severity = src.read(1).astype(float)

# The SCENFIRE logic assumes strictly positive magnitudes.
# Non-positive or invalid pixels are removed.
severity[severity <= 0] = np.nan


# ------------------------------------------------------
# 2. CONVERT RASTER → EVENT VECTORS
# ------------------------------------------------------
# Each valid raster cell is interpreted as a potential fire event.

# Fire "sizes": burn severity magnitudes extracted from the raster
sizes = severity[np.isfinite(severity)]

# Event surfaces represent exposure or weighting.
# When no spatial weighting is available, a uniform surface is assumed.
event_surfaces = np.ones_like(sizes)


# ------------------------------------------------------
# 3. CREATE DISTRIBUTION (SCENFIRE CORE ALGORITHM)
# ------------------------------------------------------
# A subset of events is selected so that their size distribution best matches a target
# power-law distribution inferred from the data.

result = scenfirepy.create_distribution(
    sizes=sizes,

    # Small deterministic jitter avoids numerical degeneracy
    # when event surfaces are uniform.
    event_surfaces=np.ones_like(sizes) + 1e-6 * np.arange(sizes.size),

    # Lower cutoff removes very small or noise-dominated values
    xmin=np.nanpercentile(sizes[sizes > 0], 5),

    # Target power-law exponent
    alpha=2.3,

    # Modest number of bins improves numerical stability
    num_bins=10,

    # Seed ensures reproducible event selection
    seed=123
)


# ------------------------------------------------------
# 4. USER-FACING OUTPUT
# ------------------------------------------------------
# The output includes the selected event magnitudes and a discrepancy metric quantifying the
# match to the target distribution.


df = pd.DataFrame({
    "selected_event_size": result["events"]
})

print("Discrepancy:", result["discrepancy"])


###### END
print(df.head())

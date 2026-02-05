<img src="scenfirepy_logo.png" alt="scenfirepy logo" width="200" align="left" style="margin-right:16px;"/>

<p>
<code>scenfirepy</code> is a Python library for constructing scenario-consistent spatial fire maps by selecting subsets of simulated or observed fire events whose size distribution matches an empirical or user-defined target. Rather than forecasting fire occurrence, the library supports scenario construction: it identifies collections of fire events whose aggregated magnitude reproduces a prescribed distribution and converts those selections into spatial weight or burn-probability rasters suitable for comparative risk, hazard, or severity analyses. 
  
<code>scenfirepy</code> conceptually shares the core logic of the SCENFIRE R package: Rodrigues M (2026). _scenfire: Post-Processing Algorithm for Integrating Wildfire Simulations_.
  doi:10.32614/CRAN.package.scenfire, R package version 0.1.0. <https://doi.org/10.32614/CRAN.package.scenfire>
    
</p>

<div style="clear: both;"></div>

## Conceptual overview

Given a sampling of candidate fire events (raster-based events or mapped perimeters), scenfirepy:
-	builds a target magnitude distribution (e.g. from observations or reference simulations);
-	repeatedly samples events without replacement, weighted by event probability;
-	stops sampling when a predefined total magnitude (surface) is reached;
-	evaluates the sampled subset against the target using an L₁ histogram discrepancy;
-	retains the subset that best matches the target distribution.
The selected events are then mapped back to space to generate per-cell scenario weights or burn-probability rasters.

## Typical applications
-	Build scenario burn-probability or weight maps from hazard or severity rasters.
-	Select scenario-consistent subsets of simulated perimeters for spatial comparison.
-	Produce inputs for exposure, impact, or relative risk analyses. 
-	Aggregate FLP20 (Fire Landscape Probability outputs) from the FConstMTT / Minimum Travel Time (MTT) fire spread model into cellwise severity rasters.
  
## Core functionality
-	Target histogram construction (linear or log-spaced bins).
-	Event selection via probability-weighted sampling without replacement.
-	Explicit magnitude control through a surface_threshold (absolute or fractional).
-	Selection quality assessed by normalized L₁ histogram discrepancy.
-	Conversion of selected events into per-event mass and spatial rasters.
-	Optional helpers for reading and aggregating FLP20 outputs.

## Primary functions:
-	build_target_hist
-	select_events
-	calc_burn_probability
-	FLP20 parsing and aggregation helpers

## Typical workflow 
-	Derive event magnitudes (sizes) and spatial supports (event_surfaces).
-	Build the target histogram from reference data.
-	Run select_events(...) with tuning parameters.
-	Convert selected events to per-event weights with calc_burn_probability(...).
-	Rasterize results to GeoTIFF or GPKG.

## Inputs and outputs
-	Inputs: rasters or vector files defining fire event magnitudes and spatial extent.
-	Outputs: per-event scenario weights and spatial rasters.
Note: the selected surface is the sum of retained event magnitudes. It represents physical area only if the input magnitudes are areas; otherwise it represents total retained magnitude in the units of the input data.

## Reproducibility and tuning
-	Use seed to reproduce a given selection.
-	Improve fit by increasing max_it / iter_limit, or by running multiple seeds and retaining the best result.
-	Scenario magnitude can be controlled directly (surface_threshold) or relatively (SURF_FRAC × reference surface).
-	Avoid excessive bin counts when data are sparse.

## Important cautions
-	Histogram comparisons require identical bin edges across runs.
-	Event ordering must be consistent between magnitude vectors and spatial representations. Misalignment will invalidate results and is a usage error, not an algorithmic flaw.
-	Outputs are scenario-relative weights, not unconditional or annualized probabilities.

## Limitations
-	The stochastic search may yield different solutions for different seeds; stability improves with iteration count or seed sweeps.
-	FLP20 functionality is limited to flame-length/severity aggregation and is not required for hazard workflows.

---

## Installation

`scenfirepy` can be installed using Anaconda and used from the Anaconda Prompt,
VS Code, or JupyterLab.

Run the following commands in an Anaconda Prompt:

    conda install -y python=3.10 numpy scipy pandas matplotlib rasterio
    pip install https://github.com/eciodiniz/scenfirepy/archive/refs/heads/main.zip
---

## Examples of scenfirepy application

- Example 1 - [Fire hazard–based scenario selection](https://github.com/eciodiniz/scenfirepy/blob/main/examples/example_01_fire_hazard.md)
- Example 2 - [Fire severity–based scenario selection](https://github.com/eciodiniz/scenfirepy/blob/main/examples/example_02_fire_severity.md)

## Status

Under active development.


## License

CC BY-NC-SA 4.0

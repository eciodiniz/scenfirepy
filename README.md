<img src="scenfirepy_logo.png" alt="scenfirepy logo" width="200" align="left" style="margin-right:16px;"/>

<p>
<code>scenfirepy</code> is a Python library for constructing scenario-consistent spatial fire maps by selecting subsets of simulated or observed fire events whose size distribution matches an empirical or user-defined target. Rather than forecasting fire occurrence, the library supports scenario construction: it identifies collections of fire events whose aggregated magnitude reproduces a prescribed distribution and converts those selections into spatial weight or burn-probability rasters suitable for comparative risk, hazard, or severity analyses. 

<code>scenfirepy</code> conceptually follows the core logic of the SCENFIRE R package: 
https://github.com/rmmarcos/SCENFIRE_package
</p>

<div style="clear: both;"></div>

This enables Python-based workflows that link fire simulation outputs to
empirically derived fire-size distributions, supporting fire-risk analysis,
scenario generation, and burn-probability studies where simulated events must
be consistent with observed fire regimes.

Thus, `scenfirepy` allows the user, for instance, to:
- process FLP20 (Fire Landscape Probability outputs) from the FConstMTT / Minimum Travel Time (MTT) fire spread model
- build target fire-size distributions
- select simulated events to match historical fire regimes
- support burn-probability and scenario analysis
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

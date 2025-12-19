# scenfirepy

scenfirepy is a Python library for building fire-size scenarios by selecting subsets
of simulated fire events whose size distributions reproduce observed historical
fire regimes. Historical regimes can be characterized using raster-based fire
information such as fire hazard, burned area, or fire severity, depending on
data availability.

The package mirrors the core logic of the SCENFIRE R package:
https://github.com/rmmarcos/SCENFIRE_package

This enables Python-based workflows that link fire simulation outputs to
empirically derived fire-size distributions, supporting fire-risk analysis,
scenario generation, and burn-probability studies where simulated events must
be consistent with observed fire regimes.

Thus, scenfirepy allows the user, for instance, to:
- process FLP20 (Fire Landscape Probability outputs) from the FConstMTT / Minimum Travel Time (MTT) fire spread model
- build target fire-size distributions
- select simulated events to match historical fire regimes
- support burn-probability and scenario analysis


## Installation

scenfirepy can be installed using Anaconda and used from the Anaconda Prompt,
VS Code, or JupyterLab.

Run the following commands in an Anaconda Prompt:

    conda install -y python=3.10 numpy scipy pandas matplotlib rasterio
    pip install https://github.com/eciodiniz/scenfirepy/archive/refs/heads/main.zip


## Examples of scenfirepy application

- Example 1 - [Fire hazard–based scenario selection](https://github.com/eciodiniz/scenfirepy/blob/main/examples/example_01_fire_hazard.md)
- Example 2 - [Fire severity–based scenario selection](https://github.com/eciodiniz/scenfirepy/blob/main/examples/example_02_fire_severity.md)

## Status

Under active development.


## License

CC BY-NC-SA 4.0

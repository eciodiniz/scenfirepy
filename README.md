# scenfirepy

`scenfirepy` is a Python implementation for building fire-size scenarios by selecting simulated fire events that reproduce a target historical fire hazard or severity, and fire-size distribution.
Depending on data availability, fire hazard, burned area, or fire severity rasters can be used as proxies for historical fire regime.

This Python library mirrors the logic of the SCENFIRE R package: https://github.com/rmmarcos/SCENFIRE_package, thus allowing the user, for instance, to:
- preprocess FLP20 / fire simulation outputs
- build target fire-size distributions
- select simulated events to match historical regimes
- support burn probability and scenario analysis


---
## Examples of scenfirepy application

- [Example 1 — Fire hazard–based scenario selection](examples/example_01_fire_hazard.md)

- [Example 2 — Fire severity–based scenario selection](examples/example_02_fire_severity.md)


## Status
Under active development.

## License
CC BY-NC-SA 4.0

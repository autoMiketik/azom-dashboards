# Project goals

**Status:** Two dashboards are packaged; live wheel verification remains.

## Scope

Create readable MOZA CS Pro and KS Pro dashboards for SimHub through AZOM, using iRacing as the first verification environment. Keep ATSR-Hub EVO in scope for wheel lighting profiles.

The current package provides Race and Settings layouts, editable and upload-ready files, a telemetry binding map, an install guide, and a downloadable ZIP. A setting change uses SimHub/AZOM formulas to show the setting name, value, and matching Settings-page accent color across the full display for five seconds. No separate runtime is required.

## Remaining verification

On the target wheel, confirm each live property path, value, units, and behavior in SimHub; verify AZOM channel mappings and the full-screen setting view; and check readability at normal driving distance. Record the simulator, car, session, wheel, firmware, software versions, and observed values in the binding map or [verification notes](docs/verification.md). Keep replay results separate from hardware results.

See the [telemetry guide](telemetry/README.md) for property lookup and [reference index](docs/REFERENCES.md) for upstream documentation.

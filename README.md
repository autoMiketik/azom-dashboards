# MOZA CS Pro / KS Pro Dashboards

Download the [dashboard package](dashboards/MOZA-CS-KS-Pro-Dashboards.zip) to import and inspect eight MOZA Dash Studio layouts: Race, Settings, and popups for ABS, Brake Bias, Traction Control, Engine Map, Engine Braking, and TC 2. The ZIP includes editable `.mzdash` files, a binding map, an optional popup controller, and a design preview.

## Files

- [Editable layouts](dashboards/editable/) and [upload-ready exports](dashboards/exports/)
- [Installation guide](dashboards/INSTALL.md)
- [Telemetry binding map](dashboards/bindings.csv)
- [Popup controller and configuration](dashboards/controller/)
- [Design preview](docs/mockups/dashboard-preview.png)
- [Dashboard plan](docs/DASHBOARD_PLAN.md) and [verification notes](docs/verification.md)

## Compatibility and verification

The layouts target MOZA CS Pro and KS Pro wheels through AZOM, with iRacing as the first telemetry environment. They are first-pass designs based on the supplied 780 × 248 sample layout. SimHub mappings and signal behavior are documented in the binding map; fuel estimates need AZOM channel mapping.

The package has not yet been imported into Dashboard Studio or exercised on a wheel. Live telemetry values, page capacity and order, physical readability, and popup switching still need checking on the target SimHub host and wheel. The installation guide lists the setup steps and the controller's requirements.

The generator is [tools/generate_dashboards.py](tools/generate_dashboards.py). It recreates the editable layouts, exports, and downloadable ZIP.

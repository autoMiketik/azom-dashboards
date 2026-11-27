# MOZA CS Pro / KS Pro Dashboards

Download the [dashboard package](dashboards/MOZA-CS-KS-Pro-Dashboards.zip) for two MOZA Dash Studio layouts: Race and Settings. A setting change temporarily takes over the full display: its name appears at the top, its value is large and centered, and the background matches that setting's accent color. The same dashboard reappears after five seconds. The display runs through SimHub and AZOM channel formulas; using the package needs no Python install, helper app, or separate background process.

## Files

- [Editable layouts](dashboards/editable/) and [upload-ready exports](dashboards/exports/)
- [Installation guide](dashboards/INSTALL.md)
- [Telemetry binding map](dashboards/bindings.csv)
- [SimHub setting-notice formula](dashboards/setting-change-notice.js)
- [Design preview](docs/mockups/dashboard-preview.png)
- [Dashboard plan](docs/DASHBOARD_PLAN.md) and [verification notes](docs/verification.md)

## Compatibility and verification

The layouts target MOZA CS Pro and KS Pro wheels through AZOM, with iRacing as the first telemetry environment. The notice uses AZOM's formula channel mappings and requires a version with that feature (AZOM 1.7.5 or newer). Fuel estimates need AZOM channel mapping as described in the installation guide.

The package has not yet been imported into Dashboard Studio or exercised on a wheel. Live telemetry values, the notice formula, physical readability, and wheel behavior still need checking on the target SimHub host and wheel.

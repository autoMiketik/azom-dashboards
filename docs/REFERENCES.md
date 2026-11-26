# Project references

These links are research sources for the initial dashboard and SimHub integration work. Confirm current versions and compatibility before relying on implementation details.

## SimHub

- [SimHub Wiki](https://github.com/SHWotever/SimHub/wiki) — general documentation for SimHub setup, supported game data, Dash Studio, plugins, and troubleshooting.
- [JavaScript Formula Engine](https://github.com/SHWotever/SimHub/wiki/Javascript-Formula-Engine) — formula syntax, per-formula scope, and state stored on `root` across evaluations.

## MOZA dashboards

- [MOZA Dash Studio Tutorial](https://support.mozaracing.com/en/support/solutions/articles/70000665526-moza-dash-studio-tutorial) — creating a dashboard, available controls, telemetry binding, and uploading a dashboard to a device.
- [`reference-dashboard.zip`](../references/reference-dashboard.zip) — local example supplied for this project. It contains an `.mzdash` named `ICONIC DASHBOARD CS KS PRO Maomi-Tom`; verify the target model before treating it as a template. The archive is excluded from Git.

## SimHub integrations and add-ons

- [AZOM](https://github.com/giantorth/AZOM) — required MOZA-to-SimHub integration. Its documentation covers wheel dashboard channels, SimHub telemetry mapping, and `.mzdash` upload; the project README lists CS Pro among tested wheels.
- [AZOM v1.7.5 formula channel mapping](https://github.com/giantorth/AZOM/blob/v1.7.5/docs/ncalc-channel-mapping.md) — uses SimHub's NCalc/JavaScript formula engine to map channel values without adding a runtime dependency.
- [AZOM wheel file guide](https://giant.orth.cc/guides/wheel-files/) — `.mzdash` upload, Dashboard Studio editing, and the distinction between firmware-rendered layouts and SimHub dashboards.
- [ATSR-Hub EVO](https://github.com/ATSR-Alex/ATSR-Hub-EVO) — required SimHub add-on, including LED profiles, telemetry-driven effects, and device profiles.

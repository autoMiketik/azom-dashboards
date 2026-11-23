# Dashboard verification

## 2026-11-23 · Transport milestone

### Local documentation check

- AZOM's [Properties & Actions reference](https://giant.orth.cc/guides/properties-and-actions/) describes `AZOM.DashboardName` as the dashboard currently on screen. Its published dashboard actions are `AZOM.DashboardNext` and `AZOM.DashboardPrev`; the list does not document direct selection by dashboard name or slot.
- AZOM's [release notes](https://github.com/giantorth/AZOM/releases) identify `AZOM.DashboardName` as added in v1.7.2. The latest release shown during this check is v1.7.5 (2026-11-23). This does not establish which version is installed on the target SimHub host.
- `references/reference-dashboard.zip` contains one `.mzdash`. Python's JSON parser accepted it; the layout metadata reports format version `1.1.1`, canvas width `780`, and height `248`. The archive does not establish how many dashboards the connected wheel supports.
- This check ran on Linux. No SimHub/AZOM installation was found under `/home/mike`, and `wine` is unavailable. There is no connected target wheel in this environment.

### Not verified

- Installed SimHub, AZOM, Dashboard Studio, wheel firmware, and ATSR-Hub EVO versions.
- Reading the active dashboard name live, selecting a specific dashboard, restoring the captured main dashboard, wheel-side confirmation, or capacity for two main and six popup slots.
- ATSR-Hub EVO lighting continuity during dashboard changes.

### Restart point

On the Windows/SimHub host with the CS Pro or KS Pro connected, record the installed versions. Upload and inspect the package layouts, then read `AZOM.DashboardName` for the active page and test selecting a popup and restoring the original main page. Verify wheel display and LED continuity and confirm whether eight slots can be enabled. If AZOM exposes only next/previous there too, decide and scope the controller integration or AZOM extension before enabling automatic popup switching. Keep replay checks and hardware checks labeled separately.

## 2026-11-23 · First-pass layout package

- Created Race, Settings, and six dedicated setting popup `.mzdash` layouts from the supplied MOZA sample schema. The editable files, upload-ready copies, generator, binding map, and installation notes are under `dashboards/` and `tools/`.
- The layouts use AZOM channel URLs from the project's SimHub catalog. Fuel-per-lap and fuel-laps are intended to use the SimHub computed estimates and need manual mapping in AZOM as recorded in `dashboards/bindings.csv`.
- The separate popup dashboards were built now so they can be imported and inspected, while transport support remains unresolved.
- Format checks accepted all eight files as JSON, confirmed the sample's 1.1.1 format version and 780 × 248 canvas, compiled all 23 dashboard formatter expressions with Node.js, confirmed all eight exports are in the ZIP, and `git diff --check` passed.
- Not verified: MOZA Dashboard Studio import/render, wheel upload, physical readability, live telemetry values/units, channel binding behavior, or the popup timer/controller. The package is ready for the user to import and inspect; these checks require their SimHub host and wheel.

## 2026-11-23 · Popup controller implementation

- Search found TrackThirtyTwo dashboards support setting-change popups and configurable popup duration ([dashboard feature page](https://www.trackthirtytwo.com/products/dashboards), [change log](https://www.trackthirtytwo.com/change-logs/simhub-dashboards)). That feature runs inside the TrackThirtyTwo dashboard/plugin system; the MOZA wheel requires AZOM-uploaded `.mzdash` pages, so it does not replace this controller.
- SimHub Property Server documents TCP property subscriptions for generic SimHub properties ([plugin docs](https://github.com/pre-martin/SimHubPropertyServer/blob/main/doc/PropertyServer/PropertyServer.adoc)); SimHub documents `-triggeraction` on its running process ([CLI reference](https://github.com/SHWotever/SimHub/wiki/Command-line-interface)). AZOM publishes `AZOM.DashboardName`, `AZOM.DashboardNext`, and `AZOM.DashboardPrev` ([AZOM actions reference](https://giant.orth.cc/guides/properties-and-actions/)). The controller joins these interfaces without modifying AZOM.
- Added `dashboards/controller/dashboard_controller.py`, `controller.json`, and a Windows launcher. The helper baselines settings, rounds to configured precision, ignores negative sentinel values for discrete settings while allowing negative brake bias, captures the main page, cycles to popups, restarts one configurable timer, restores the main page, cancels on manual main-page changes, and skips popup pages during normal navigation.
- The gear cue color uses AZOM's documented `CarSettings_RPMShiftLight2` 0–1 progress property and a channel formula that excludes neutral, reverse, and top gear ([AZOM SimHub property reference](https://github.com/giantorth/AZOM/blob/main/docs/simhub.md#pluginmanager-properties)). The formula is listed in `dashboards/bindings.csv`.
- The Windows SimHub host must have SimHub, AZOM, Python 3.10+, and SimHub Property Server enabled. Upload/enable the eight dashboards in their configured order. Direct name selection is still not documented, so page names/order and the cyclic next/previous behavior need verification against the actual wheel. No hardware exercise is recorded yet.
- Format checks passed for both Python files (AST parse), controller JSON, the 18-row binding CSV, all eight editable/export pairs, and ZIP contents/integrity. No runtime tests were run, per the requested workflow.

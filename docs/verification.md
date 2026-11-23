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

On the Windows/SimHub host with the CS Pro or KS Pro connected, record the installed versions. Read `AZOM.DashboardName` for the active page, test selecting a named popup and restoring the original main page, then verify wheel display and LED continuity. Confirm whether eight slots can be enabled. If AZOM exposes only next/previous there too, decide and scope the controller integration or AZOM extension before building popup dashboards. Keep replay checks and hardware checks labeled separately.

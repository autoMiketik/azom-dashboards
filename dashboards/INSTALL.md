# Installation guide

This package contains eight MOZA Dash Studio `.mzdash` layouts, a telemetry binding map, an optional popup controller, and a design preview. Review each dashboard in MOZA Dashboard Studio before uploading it to the wheel.

## Upload the dashboards

1. Extract this ZIP.
2. In SimHub, open AZOM, select the connected MOZA wheel under Devices, and open Files.
3. Choose each `.mzdash` file from the extracted folder and upload it. Enable the dashboards you want on the wheel.
4. Open the layouts in MOZA Dashboard Studio to inspect or edit them. `dashboard-preview.png` shows the design overview; use Studio's device preview to inspect the wheel rendering.
5. In AZOM's Dashboard & Channels view, inspect every bound channel. Map `v1/gameData/FuelConsumeLap` to `DataCorePlugin.Computed.Fuel_LitersPerLap`, `v1/gameData/FuelLaps` to `DataCorePlugin.Computed.Fuel_RemainingLaps`, and `v1/gameData/CarSettings_RPMShiftLight2` to the formula in `bindings.csv`. The binding map lists the channels, formats, and current verification state.

See AZOM's [wheel files guide](https://giant.orth.cc/guides/wheel-files/) for local `.mzdash` upload and Dashboard Studio editing. Exact signal availability, units, sign, and conversion depend on the installed versions and active car. Confirm them against live telemetry before relying on a value.

## Optional popup controller

The controller watches SimHub properties and invokes AZOM's dashboard actions when a setting changes. It requires Windows, SimHub 9.12 or newer, AZOM, Python 3.10+, and the third-party [SimHub Property Server](https://github.com/pre-martin/SimHubPropertyServer) plugin. Install and enable the plugin in SimHub; its default TCP port is 18082.

1. Upload the dashboards and enable all eight in the order in `controller/controller.json`. The wheel must support the configured slots; confirm this on the target device.
2. Check that `AZOM.DashboardName` reports the uploaded titles. If titles or wheel order differ, edit `dashboard_order` in `controller/controller.json` to match.
3. Set `simhub_exe` in `controller/controller.json` if SimHub is installed elsewhere.
4. Run `controller/run_controller.bat` on the SimHub host and keep the console open while driving.

The controller uses one five-second popup timer, seeds each setting from its first valid sample, and returns to the main dashboard captured when the popup sequence began. AZOM's published interface exposes next/previous dashboard actions and the active dashboard name, but does not document direct named-dashboard selection. The controller therefore follows the configured slot order. Verify page order, popup selection, restoration, telemetry, and wheel behavior on the actual setup before relying on automatic switching.

The layouts are first-pass designs based on a supplied 780 × 248 sample. Dashboard Studio import/rendering, live values, physical readability, page capacity, and controller operation have not yet been confirmed on a target wheel.

# Installation guide

This package contains two MOZA Dash Studio `.mzdash` layouts, a telemetry binding map, the SimHub formula for setting-change notices, and a design preview. It uses SimHub with the AZOM plugin. You do not need Python, SimHub Property Server, or a separate helper program to use it.

## Upload the dashboards

1. Extract this ZIP.
2. In SimHub, open AZOM, select the connected MOZA wheel under Devices, and open Files.
3. Upload `01-race.mzdash` and `02-settings.mzdash`. Enable both layouts.
4. Open the layouts in MOZA Dashboard Studio to inspect or edit them. `dashboard-preview.png` shows the design overview; use Studio's device preview to inspect the wheel rendering.
5. In AZOM's Dashboard & Channels view, inspect each bound channel. Map `v1/gameData/FuelConsumeLap` to `DataCorePlugin.Computed.Fuel_LitersPerLap`, `v1/gameData/FuelLaps` to `DataCorePlugin.Computed.Fuel_RemainingLaps`, and `v1/gameData/CarSettings_RPMShiftLight2` to the formula in `bindings.csv`.

## Set up setting-change notices

When one of the six supported settings changes, a full-screen view shows the setting name at the top and its value in large type at the center for five seconds. The background uses the same accent color as that setting's line on the Settings page, with dark text for contrast. The overlay then clears to reveal the same Race or Settings dashboard. It does not switch dashboard slots or require another running program.

1. In AZOM's Dashboard & Channels view, open the channel mappings for **MOZA Race**.
2. Map `v1/gameData/SessionTypeName` to the final `js:` line in `setting-change-notice.js` (leave out the comment lines).
3. Repeat the same mapping for **MOZA Settings**.
4. To change the shared duration, edit `durationMs` in the formula, then paste the same updated formula into both mappings.

The formula seeds its first telemetry sample as a baseline, ignores negative/unavailable values for discrete settings while preserving zero, normalizes brake bias for display, and replaces the view when another setting changes. Each new change restarts the five-second timer. It resets its baseline when the game, car, track, session, or restart state changes. If several settings change in one telemetry update, the last setting in the order listed in `bindings.csv` is shown.

AZOM 1.7.5 or newer is required for formula channel mappings. SimHub and AZOM evaluate the formula as part of their normal telemetry flow; no console or additional process needs to stay open.

See AZOM's [wheel files guide](https://giant.orth.cc/guides/wheel-files/) for `.mzdash` upload and Dashboard Studio editing. Exact signal availability, units, sign, and conversion depend on installed versions and the active car. Confirm them against live telemetry before relying on a value.

The layouts are first-pass designs based on a supplied 780 × 248 sample. Dashboard Studio import/rendering, live values, physical readability, and notice timing have not yet been confirmed on a target wheel.

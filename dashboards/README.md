# MOZA CS Pro / KS Pro dashboard package

The downloadable bundle contains eight editable MOZA Dash Studio `.mzdash` files: Race, Settings, and one popup each for ABS, Brake Bias, Traction Control, Engine Map, Engine Braking, and TC 2. The editable and export copies are identical. `MOZA-CS-KS-Pro-Dashboards.zip` also includes this install guide, the binding map, and the design preview.

## Install and inspect

1. Download and extract `MOZA-CS-KS-Pro-Dashboards.zip`.
2. In SimHub, open AZOM, select the connected MOZA wheel under Devices, then open Files.
3. Choose each local `.mzdash` file and upload it. Enable the dashboards you want on the wheel.
4. Open the project copies in MOZA Dashboard Studio to inspect or edit them. The included `../docs/mockups/dashboard-preview.png` is the design overview; Studio's device preview is the right place to inspect the actual wheel rendering.
5. In AZOM's Dashboard & Channels view, inspect the mapping for every bound channel. Map `v1/gameData/FuelConsumeLap` to `DataCorePlugin.Computed.Fuel_LitersPerLap`, `v1/gameData/FuelLaps` to `DataCorePlugin.Computed.Fuel_RemainingLaps`, and `v1/gameData/CarSettings_RPMShiftLight2` to the formula in `bindings.csv`. The files use AZOM channel URLs and SimHub formulas; exact availability, sign, units, and conversions depend on the installed versions and active iRacing car. `bindings.csv` lists all channels and required mappings.

AZOM's upload guide documents local `.mzdash` upload and Dashboard Studio editing: <https://giant.orth.cc/guides/wheel-files/>.

## What is included

- `editable/`: editable source layouts.
- `exports/`: matching `.mzdash` files, ready for local upload.
- `bindings.csv`: source channel, display use, formatting, and verification state for each signal.
- `controller/`: SimHub Property Server bridge, its configuration, and Windows launcher for change-triggered popups.
- `MOZA-CS-KS-Pro-Dashboards.zip`: convenient install bundle.
- `../tools/generate_dashboards.py`: regenerates the editable files, exports, and bundle from the supplied MOZA `.mzdash` sample.

These are first-pass layouts derived from the supplied CS/KS Pro sample's 780 × 248 canvas and widget schema. The sample declares Dashboard Studio format version 1.1.1 and uses Manrope3. Review the layouts in Studio before uploading; this environment cannot run Studio or confirm physical readability.

## Popup controller setup

The package includes a controller that reads SimHub properties and invokes AZOM's documented dashboard actions. It needs Windows, SimHub 9.12 or newer, AZOM, Python 3.10+, and the third-party [SimHub Property Server](https://github.com/pre-martin/SimHubPropertyServer) plugin. Install the plugin DLL in SimHub's folder and enable it in Settings › Plugins; Property Server requires SimHub 9.6 or newer and its default TCP port is 18082.

1. Upload and enable all eight dashboards in the order listed in `controller/controller.json`. Disable other wheel dashboard slots while using this controller so its cycle order stays accurate.
2. Confirm the active wheel reports each uploaded name through `AZOM.DashboardName`. If AZOM uses a different title, edit `dashboard_order` in `controller.json` to match the names and actual wheel order.
3. Set `simhub_exe` in `controller.json` if SimHub is not at the default install path.
4. Run `controller/run_controller.bat` on the SimHub host. The console logs active pages, observed setting changes, popup replacement, timer expiry, and action failures. Keep it running while driving.

The controller seeds each setting from its first valid sample, ignores unavailable negative values, preserves zero, rounds settings to their configured display precision, and resets its baselines at game, car, session-restart, or wheel disconnect changes. It keeps the first main page as the return target through repeated or mixed popup changes, restarts one shared five-second timer, and cancels restoration if a manual main-page change occurs. When no popup sequence is active, it skips popup slots during normal next/previous navigation by routing to the nearest main page.

AZOM's documented interface exposes next/previous dashboard actions and the active dashboard name, but no direct named-dashboard selection. The controller therefore follows the configured slot order and checks each page change before continuing. Page order must match the connected wheel. The gear color binding uses AZOM's documented `CarSettings_RPMShiftLight2` progress channel; the mapping formula excludes neutral, reverse, and top gear. Hardware behavior, setting availability, physical readability, and LED continuity still need a live check.

The design plan describes the intended behavior and the required checks in `../docs/DASHBOARD_PLAN.md`; `../docs/verification.md` records the current transport evidence and restart point.

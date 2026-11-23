# MOZA CS Pro / KS Pro dashboard package

The downloadable bundle contains eight editable MOZA Dash Studio `.mzdash` files: Race, Settings, and one popup each for ABS, Brake Bias, Traction Control, Engine Map, Engine Braking, and TC 2. The editable and export copies are identical. `MOZA-CS-KS-Pro-Dashboards.zip` also includes this install guide, the binding map, and the design preview.

## Install and inspect

1. Download and extract `MOZA-CS-KS-Pro-Dashboards.zip`.
2. In SimHub, open AZOM, select the connected MOZA wheel under Devices, then open Files.
3. Choose each local `.mzdash` file and upload it. Enable the dashboards you want on the wheel.
4. Open the project copies in MOZA Dashboard Studio to inspect or edit them. The included `../docs/mockups/dashboard-preview.png` is the design overview; Studio's device preview is the right place to inspect the actual wheel rendering.
5. In AZOM's Dashboard & Channels view, inspect the mapping for every bound channel. Map `v1/gameData/FuelConsumeLap` to `DataCorePlugin.Computed.Fuel_LitersPerLap` and `v1/gameData/FuelLaps` to `DataCorePlugin.Computed.Fuel_RemainingLaps` if those SimHub computations are available. The files use AZOM channel URLs and SimHub formulas; exact availability, sign, units, and conversions depend on the installed versions and active iRacing car. `bindings.csv` lists all channels and required mappings.

AZOM's upload guide documents local `.mzdash` upload and Dashboard Studio editing: <https://giant.orth.cc/guides/wheel-files/>.

## What is included

- `editable/`: editable source layouts.
- `exports/`: matching `.mzdash` files, ready for local upload.
- `bindings.csv`: source channel, display use, formatting, and verification state for each signal.
- `MOZA-CS-KS-Pro-Dashboards.zip`: convenient install bundle.
- `../tools/generate_dashboards.py`: regenerates the editable files, exports, and bundle from the supplied MOZA `.mzdash` sample.

These are first-pass layouts derived from the supplied CS/KS Pro sample's 780 × 248 canvas and widget schema. The sample declares Dashboard Studio format version 1.1.1 and uses Manrope3. Review the layouts in Studio before uploading; this environment cannot run Studio or confirm physical readability.

## Popup behavior status

Each popup is a separate dashboard and reads its setting channel live. The layouts do not contain a change detector, shared five-second timer, saved main-page return target, or automatic page switching. Those behaviors need a controller on the SimHub host and must be exercised with the wheel. The gear digit also remains neutral white; the live shift-cue channel and dynamic color binding still need to be established. AZOM's published actions expose next/previous dashboard switching and an active dashboard name, but no direct named-dashboard selection. The layouts are ready to inspect while those integrations remain to be solved during hardware troubleshooting.

The design plan describes the intended behavior and the required checks in `../docs/DASHBOARD_PLAN.md`; `../docs/verification.md` records the current transport evidence and restart point.

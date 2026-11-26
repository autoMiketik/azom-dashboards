# MOZA dashboard design plan

Design draft for review. The prototype targets iRacing through SimHub and AZOM, with ATSR-Hub EVO handling the wheel lighting profile. The CS Pro and KS Pro are the target wheels. The supplied CS/KS Pro reference layout declares a **780 × 248 px** canvas. Use that for the mockups and confirm the dimensions, usable edges, and font in Dashboard Studio and on each wheel before export. [MOZA display overview](https://eu.mozaracing.com/es/blogs/news/moza-racing-ces-2026-porsche-mission-r-wheel) · [AZOM authoring and upload](https://giant.orth.cc/guides/wheel-files/)

![Race and Settings dashboards with a setting-change notice](mockups/dashboard-preview.png)

## Visual rules

Use a flat charcoal background `#0D1117`, near-white values `#F4F7FB`, muted labels `#AEBBCA`, and subtle rules `#34404D`. Use a legible sans serif with tabular digits, bold numerals, and short uppercase labels. The preview uses Noto Sans. Match its numeral widths in Dashboard Studio with a font the wheel supports. Use a 20 px left and right inset and keep text away from the corners. Color supports signed values and named states. Avoid blinking, gradients, and decorative badges.

Sizes below are design targets in canvas pixels. Test the design at physical size from the normal driving position. For a roughly 3-inch diagonal, the complete 780 px canvas is about 72 mm wide. Use the physical wheel to decide whether any secondary information needs its own page.

## Main 1 · Race

The center carries the quickest glances. Timing stays on the left and fuel stays on the right. Coordinates are from the top-left of the canvas. Vertical positions for text in this plan are baselines.

| Area | Placement and size | Content |
| --- | --- | --- |
| Header | x 20 and x 760, y 34. Values 26 px | Overall position left, such as `P7`. Session time remaining right, such as `24:36`, with hours when needed. |
| Timing | x 20–239, labels at y 66, 120, 174. Values at y 96, 150, 204 | Current lap at 30 px, last and best at 28 px. Display `m:ss.sss`; allow multiple minute digits. |
| Driving | Center x 390, speed baseline y 79, gear y 175 | Speed at 34 px with `km/h` at 16 px. Gear at 100 px, including `N` and `R`. Switch the gear digit to steady red `#FF5967` while the shift cue is active. |
| Live delta | Center x 390, label y 199 and value y 230 | `Δ VS SESSION BEST` at 16 px and signed seconds at 34 px, e.g. `−0.28 s`. Mint `#71E6AD` for quicker, rose `#FF8994` for slower, white at zero. |
| Fuel | Right align at x 760, same three rows as timing | Fuel remaining `36.4 L`, consumption `2.83 L/lap`, and estimated laps on fuel `12.9 laps`. Labels at 16 px, numbers at 30 px, units at 16 px. |

Prefer the signed live delta because it answers whether the current lap is gaining or losing time at this point on track. Use a valid session-best reference and show a dash when the reference is unavailable. Keep the shift and flag LEDs on the ATSR-Hub EVO profile. Keep maps, pedal graphs, rival lists, and four-corner tyre data off this default page. Class position and laps to go are useful candidates for a later race strategy page. [iRacing timing, relative, and fuel displays](https://support.iracing.com/support/solutions/articles/31000167257-black-box-screen-information-and-controls) · [iRacing delta reference modes](https://support.iracing.com/support/solutions/articles/31000133605-clear-split-deltas-from-the-sim) · [AZOM and ATSR lighting](https://giant.orth.cc/guides/)

### Shift cue

Use the active car and gear shift cue that drives the ATSR-Hub EVO LEDs through AZOM if the installed setup exposes it for dashboard binding. Change the digit color immediately when the cue becomes active. Restore near-white when it clears or the driver shifts. Leave flashing to the LEDs. Keep the digit neutral in `N`, `R`, top gear, or when the cue or top-gear status cannot be determined. [ATSR-Hub EVO shift light release notes](https://github.com/ATSR-Alex/ATSR-Hub-EVO/releases)

If the shared LED cue is unavailable, bind the AZOM dashboard channel to SimHub's `DataCorePlugin.GameData.CarSettings_RPMRedLineReached`. Treat that fallback as a redline warning. It may activate later than the shift LEDs. Verify the source in iRacing by comparing the digit with the LEDs in two forward gears, checking that red clears after an upshift, and confirming the neutral exclusions. [AZOM SimHub property reference](https://github.com/giantorth/AZOM/blob/main/docs/simhub.md)

### Race bindings to verify

Shared paths below are relative to `DataCorePlugin.GameData.` unless written in full. Confirm the mapping and units in the installed versions before authoring the final wheel files. [Project SimHub property map](../telemetry/simhub.csv)

| Display | Preferred SimHub property | Presentation and checks |
| --- | --- | --- |
| Gear and speed | `Gear`, `SpeedKmh` | Integer gear with neutral and reverse labels, whole km/h independent of preferred local units. |
| Current, last, and best lap | `CurrentLapTime`, `LastLapTime`, `BestLapTime` | Convert to seconds if the wheel channel expects them. Blank last or best until a usable lap exists. |
| Position and session time | `Position`, `SessionTimeLeft` | Overall position. Show a dash if the session lacks a meaningful time limit. |
| Live lap delta | `DeltaToSessionBest` | Verify sign, scale, reference, and validity. iRacing fallback candidates are `LapDeltaToSessionBestLap` and its `_OK` flag. |
| Fuel remaining | `Fuel` | Verify litres with the installed SimHub configuration and actual AZOM channel. |
| Fuel per lap and estimated laps | `DataCorePlugin.Computed.Fuel_LitersPerLap`, `DataCorePlugin.Computed.Fuel_RemainingLaps` | Bind SimHub's estimates to suitable AZOM channels. Confirm scale and precision on the wheel. Show a dash while consumption history is insufficient. |

If the cockpit check fails, split Race into **Drive** and **Timing & Fuel**. Keep gear, speed, position, live delta, and estimated fuel laps on Drive. Put current, last, and best lap in a wide left column on Timing & Fuel, and fuel remaining, consumption per lap, and estimated laps in the right column. Keep session time in its header. Use the freed space to increase secondary values to 36 px or larger. Confirm a deliberate main-page switch; the setting-change notice stays with whichever page is active.

## Main 2 · Settings

Use a three-column, two-row grid. Column centers are x 144, 390, and 636. Labels sit at y 42 and 136 in 16 px; values use 44 px. Place brake bias top center for the easiest glance. Keep the charcoal background and neutral text across all six tiles. Center a 44 × 3 px accent line below each value. Each line uses that setting's accent color. Keep tile positions and cues stable when a setting is unavailable. Leave a narrow header area for the setting-change notice.

| Row | Left | Middle | Right |
| --- | --- | --- | --- |
| Top | ABS | Brake Bias | Traction Control |
| Bottom | Engine Map | Engine Braking | TC 2 |

Engine Braking and TC 2 are the two additional settings on this page. Keep front/rear anti-roll bar and fuel mixture as candidates for a later settings page or a car-specific binding once their meaning is confirmed. Show `—` for unavailable values and `OFF` only when the car confirms an off state. iRacing can expose different in-car adjustments by car. [iRacing in-car adjustments](https://support.iracing.com/support/solutions/articles/31000167257-black-box-screen-information-and-controls) · [Project SDK catalog](../telemetry/iracing.csv)

## Setting-change notice

Show one compact text notice in the header of both main dashboards. It displays the latest setting name and value for five seconds, then clears. A newer setting change replaces the current notice and restarts the same timer. The dashboard page stays selected; manual page navigation uses AZOM's normal wheel actions.

Use the string channel `v1/gameData/SessionTypeName` for the notice text. In AZOM's per-dashboard channel mappings, map it to the same formula from [`dashboards/setting-change-notice.js`](../dashboards/setting-change-notice.js) on Race and Settings. AZOM resolves formula mappings through SimHub's own formula engine, including JavaScript and per-formula state. This keeps the change detector and timer inside SimHub and removes the separate Python controller and Property Server dependency. [AZOM formula channel mapping](https://github.com/giantorth/AZOM/blob/v1.7.5/docs/ncalc-channel-mapping.md) · [SimHub JavaScript formula engine](https://github.com/SHWotever/SimHub/wiki/Javascript-Formula-Engine)

| Setting | SimHub property | Display |
| --- | --- | --- |
| ABS | `ABSLevel` changes | Confirmed setting or `OFF`. Compare `dcABS` if needed. ABS engagement is a separate signal. |
| Brake Bias | `BrakeBias` changes by one displayed step | Front bias percentage such as `56.2%` once validated. Compare `dcBrakeBias` against the cockpit. Some values may require a car-specific interpretation. |
| Traction Control | `TCLevel` changes | Confirmed setting or `OFF`. Compare `dcTractionControl` if needed. TC engagement is a separate signal. |
| Engine Map | `ECUMap` changes | Confirmed map number or short label. Check `dcEnginePower` only if it tracks the same cockpit control for the car. |
| Engine Braking | `EngineBrake` changes | Confirmed step or short label. Compare `dcEngineBraking` if needed. |
| TC 2 | `TC_B` changes | Confirmed second TC adjustment. Compare `dcTractionControl2` if needed. |

The formula seeds the first sample as a baseline, treats zero as valid, suppresses unavailable negative discrete values, normalizes brake bias to its displayed precision, and refreshes the notice on the latest changed setting. It resets its baseline on game, car, track, session, or restart changes. If several values change in one update, the final setting in the table order wins. The shared duration is **5.0 s** in `setting-change-notice.js`.

## Implementation and verification

The package contains two dashboards: Race and Settings. Their formats and bindings are recorded in [the package overview](../README.md), [binding map](../dashboards/bindings.csv), and [installation guide](../dashboards/INSTALL.md). The inline notice uses AZOM formula mappings and the SimHub formula engine; it does not cycle dashboard slots.

1. Upload both pages on the SimHub host and verify their appearance in MOZA Dashboard Studio and on the wheel.
2. Apply the same notice formula to the `SessionTypeName` channel mapping on both pages. In iRacing, confirm the first telemetry sample does not trigger a notice and changes from wheel controls, keyboard, and in-game menus do.
3. Check repeated changes, mixed changes, zero, unavailable values, brake-bias sign and units, the five-second timeout, and resets on session/car changes. Label replay checks and hardware checks separately in the results.
4. Read the wheel at normal driving distance in daylight and low light. Check the Race page's gear/delta and the Settings page's six values. Record car, wheel, firmware, SimHub/AZOM versions, observed values, and checks performed. See [dashboard verification](verification.md) for the current evidence and restart point.

For design review, the two decisions are whether the dense Race page reads comfortably at wheel size, and whether Engine Braking and TC 2 are the best two extra settings for the cars you drive.

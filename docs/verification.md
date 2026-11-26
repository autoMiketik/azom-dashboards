# Dashboard verification

## 2026-11-26 · SimHub-native notice design

### Documentation check

- AZOM v1.7.5 documents formula expressions for wheel channel mappings and reuses SimHub's own formula engine. Its v1.7.5 source evaluates formulas for both numeric and string channels, which allows a string channel to carry the notice text: [AZOM formula mapping](https://github.com/giantorth/AZOM/blob/v1.7.5/docs/ncalc-channel-mapping.md) · [string resolver in v1.7.5](https://github.com/giantorth/AZOM/blob/v1.7.5/Telemetry/SimHubPropertyResolver.cs).
- SimHub's JavaScript formula engine supports state across formula evaluations through `root`: [SimHub JavaScript formula documentation](https://github.com/SHWotever/SimHub/wiki/Javascript-Formula-Engine).
- AZOM's wheel file guide says layouts are rendered by wheel firmware and AZOM streams mapped SimHub telemetry to them: [AZOM wheel files and dashboard upload](https://giant.orth.cc/guides/wheel-files/).
- The previous design used a Python process and SimHub Property Server to switch between eight dashboard slots. That controller has been removed. The current design draws a full-screen overlay over the selected Race or Settings page using SimHub/AZOM formulas, then reveals the same page again when the timer expires.

### Included behavior

- Two dashboards: Race and Settings.
- Both use the `v1/gameData/SessionTypeName` string channel for the overlay text and conditional full-screen backing. Apply the same formula from `dashboards/setting-change-notice.js` to that channel on each dashboard in AZOM.
- The formula seeds an initial baseline, treats zero as a valid discrete setting, ignores unavailable negative values for discrete settings, normalizes brake bias, and shows the latest detected setting for five seconds. Game, car, track, session, and restart changes reset its baseline.
- No Python runtime, Property Server, console window, or separate helper process is required. Python remains only as a maintainer-side layout/ZIP generator in `tools/`.

### Not verified

- The formula has not been run against a connected SimHub/AZOM installation or the target CS Pro/KS Pro wheel.
- Live iRacing property behavior, brake-bias sign/scale, string-channel mapping, same-frame multi-setting tie-break, five-second timing, dynamic background-color binding, and wheel text rendering need a live check.
- Dashboard Studio import/rendering, wheel-side readability, and ATSR-Hub EVO lighting continuity remain unverified.

### Restart point

On the target SimHub host, record SimHub and AZOM versions and confirm AZOM supports formula channel mappings. Upload the two package dashboards. Apply the same formula to `SessionTypeName` on Race and Settings, then verify baseline seeding, one change, repeated changes inside five seconds, expiry, and session/car reset. Check brake bias against the iRacing cockpit and separate replay observations from hardware observations. Record the car, wheel, firmware, plugin versions, and observed values.

## Superseded prototype history · 2026-11-23

The first package contained Race, Settings, and six dedicated popup layouts. A Python controller using SimHub Property Server monitored settings and cycled AZOM's next/previous dashboard actions. The design was replaced on 2026-11-26 after the user rejected the extra runtime requirement. Its files and package instructions have been removed; the earlier hardware and telemetry checks were not performed.

Web research also found setting-change popup features in the TrackThirtyTwo SimHub dashboard system. That system does not render on MOZA wheel firmware; AZOM converts dashboard layouts to `.mzdash` and streams telemetry into those layouts. It did not remove the need for a MOZA-compatible solution.

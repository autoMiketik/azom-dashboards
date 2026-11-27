# Dashboard verification

## 2026-11-27 · Full-screen SimHub-native setting view

### Documentation check

- AZOM v1.7.5 documents formula expressions for wheel channel mappings and reuses SimHub's own formula engine. Its v1.7.5 source evaluates formulas for both numeric and string channels, which allows a string channel to carry the notice text: [AZOM formula mapping](https://github.com/giantorth/AZOM/blob/v1.7.5/docs/ncalc-channel-mapping.md) · [string resolver in v1.7.5](https://github.com/giantorth/AZOM/blob/v1.7.5/Telemetry/SimHubPropertyResolver.cs).
- SimHub's JavaScript formula engine supports state across formula evaluations through `root`: [SimHub JavaScript formula documentation](https://github.com/SHWotever/SimHub/wiki/Javascript-Formula-Engine).
- AZOM's wheel file guide says layouts are rendered by wheel firmware and AZOM streams mapped SimHub telemetry to them: [AZOM wheel files and dashboard upload](https://giant.orth.cc/guides/wheel-files/).
- The current design draws a full-screen, accent-colored overlay over the selected Race or Settings page using SimHub/AZOM formulas, then reveals the same page again when the timer expires.

### Included behavior

- Two dashboards: Race and Settings.
- Both use the `v1/gameData/SessionTypeName` string channel for the setting name, value, and matching accent color. Apply the same formula from `dashboards/setting-change-notice.js` to that channel on each dashboard in AZOM.
- The formula seeds an initial baseline, treats zero as a valid discrete setting, ignores unavailable negative values for discrete settings, normalizes brake bias, and shows the latest detected setting for five seconds. Game, car, track, session, and restart changes reset its baseline.
- No Python runtime, Property Server, console window, or separate helper process is required.

### Not verified

- The formula has not been run against a connected SimHub/AZOM installation or the target CS Pro/KS Pro wheel.
- Live iRacing property behavior, brake-bias sign/scale, string-channel mapping, same-frame multi-setting tie-break, five-second timing, dynamic accent-color background binding, text contrast, and wheel rendering need a live check.
- Dashboard Studio import/rendering, wheel-side readability, and ATSR-Hub EVO lighting continuity remain unverified.

### Restart point

On the target SimHub host, record SimHub and AZOM versions and confirm AZOM supports formula channel mappings. Upload the two package dashboards. Apply the same formula to `SessionTypeName` on Race and Settings, then verify baseline seeding, one change, repeated changes inside five seconds, expiry, and session/car reset. Check brake bias against the iRacing cockpit and separate replay observations from hardware observations. Record the car, wheel, firmware, plugin versions, and observed values.

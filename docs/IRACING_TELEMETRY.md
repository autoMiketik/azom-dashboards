# iRacing telemetry for the Brake Bias popup

## Published field list

The [iRacing live telemetry appendix (PDF)](https://us.v-cdn.net/6034148/uploads/8DD84H30FIC8/telemetry-11-23-15.pdf) catalogs SDK fields with their types, units where specified, and whether they are available live or on disk. It lists `dcBrakeBias` as a floating point in-car adjustment available in both streams for cars that expose it. The same section lists `dcABS`, `dcTractionControl`, and `dcAntiRollFront` as candidates for future popups. The appendix dates to 2015. Use it to identify candidate SDK fields and check their current SimHub paths and values in a live session.

## SimHub property lookup

Use SimHub's live property list to check what a simulator exposes for the current car and session. SimHub lists common properties alongside simulator specific properties. In the Dash Studio binding editor, use **Insert property** and enable **Show game specific properties**. [SimHub binding documentation](https://github.com/SHWotever/SimHub/wiki/Dash-Studio---Bindings)

## First live check

1. Start an iRacing Test Drive in a car with adjustable brake bias. Get into the cockpit and confirm SimHub is receiving live values such as RPM or gear.
2. Open **Available Properties** in SimHub and search for `bias`. Look for the raw iRacing telemetry field `dcBrakeBias` and any common brake bias property. Use the exact property path shown by your installation. [iRacing SDK wrapper telemetry definitions](https://github.com/vipoo/iRacingSDK.Net/blob/master/DataFeed/GeneratedTelemetry.cs)
3. Note the value before changing anything. Adjust brake bias one step up and one step back down. Compare the SimHub values with the in-car display and confirm the value holds steady between adjustments. A field under `SessionData.CarSetup` may describe the starting setup, so use a property only once it follows both live changes.
4. Record the car, SimHub version, full property path, and the before, up, and down values from SimHub and the car. If SimHub shows a fraction or a relative adjustment, use the comparison to determine how the popup should format it. A missing or unchanging field is a result for that car and session.
5. If available, use SimHub's **Record** and **Replay** to save a short sequence with two adjustments less than five seconds apart, followed by at least six seconds of steady telemetry. Confirm Replay reproduces the chosen property's values before using it to develop the popup timer. [SimHub record and replay documentation](https://github.com/SHWotever/SimHub/wiki/NCalc-scripting---Introduction)

The property path, units, and change behavior remain unverified on the first test car.

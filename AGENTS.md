# Development instructions

## Start here

- Read [PROJECT_GOALS.md](PROJECT_GOALS.md) for current scope and verification status, [the telemetry guide](telemetry/README.md) for property lookup, and [the references](docs/REFERENCES.md) for upstream documentation.
- Target MOZA CS Pro and KS Pro with SimHub, AZOM, and ATSR-Hub EVO. Use iRacing as the first verification environment and keep dashboard bindings reusable across simulators where the data supports it.

## Telemetry and layouts

- Start with [SimHub shared and computed properties](telemetry/simhub.csv). Reuse SimHub calculations, including fuel estimates, when they meet the dashboard's needs. Consult the [iRacing SDK catalog](telemetry/iracing.csv) when a shared property is missing or behaves differently. Keep any simulator-specific fallback in the binding logic so the layout can be reused.
- Treat catalog entries as source evidence. Before relying on a binding, confirm the exact property path, value, units, and behavior in SimHub. Record the simulator, car, session, software versions, and an observed value in the map or linked verification notes. If a signal is unavailable, handle that explicitly. Zero can be a valid value.
- Map the selected properties through AZOM to the channels the `.mzdash` layout uses. Confirm the channel and any conversion on the target wheel. Record which wheel was exercised. Keep editable layouts and configuration alongside the exports needed to install them. Keep local captures and third-party samples under ignored `references/`.

## Setting-change view behavior

- Use a full-screen overlay on the currently selected dashboard, with the setting name at the top, a large centered value, and the same accent color used for that setting on the Settings page. Keep the overlay visible for five seconds after the latest change.
- Use the first valid telemetry sample as a baseline. Show a real setting change, restart the timer on another change, then clear the overlay to reveal the same dashboard. Do not add a separate runtime or dashboard-switching process.
- Verify the AZOM formula mapping, accent-color background, single and repeated changes, and clearing after the timeout. Label replay checks and hardware checks separately in the results.

# Project goals

**Status:** Initial scope; refine as hardware, games, and add-ons are confirmed.

## Aim

Create useful dashboards for the MOZA CS Pro and KS Pro wheels, using SimHub telemetry with AZOM and ATSR-Hub EVO as required integrations.

## Initial goals

- Design clear, readable dashboard layouts for the wheel's display.
- Use AZOM to connect SimHub telemetry to the MOZA wheel dashboards.
- Include ATSR-Hub EVO in the required SimHub integration scope.
- Confirm the dashboard format and upload workflow for the target wheel.
- Document setup, compatibility, installation, and customization so the dashboards are practical to use and maintain.
- Validate the result on the target wheel with the selected simulator and add-ons.

## First milestone: Brake Bias popup

- When the simulator reports a change in brake bias through SimHub, select a dedicated popup dashboard on the wheel. Show **BRAKE BIAS** and the current value in large type at the center of the screen.
- Keep one shared popup duration setting, defaulting to 5 seconds. Each change updates the value and restarts the timer. The initial telemetry reading establishes a baseline.
- Remember the active main dashboard when the first popup opens. If another setting changes while a popup is visible, show the latest popup and restart the shared timer. Keep the same main dashboard as the return target.
- When the timer expires, restore the saved main dashboard. For example, with a change at 0 seconds and another at 3 seconds, restore the main dashboard at 8 seconds.

Start with one simulator, one main dashboard and one brake bias popup. Verify that SimHub exposes the setting and that AZOM can identify the active dashboard, select the popup, and restore the saved dashboard. The public [AZOM action reference](https://giant.orth.cc/guides/properties-and-actions/) documents next and previous actions. Confirm whether the installed version exposes direct selection and active dashboard state before building more layouts.

## Decisions to confirm

- CS Pro and KS Pro are confirmed compatible target wheels.
- Display constraints and dashboard behavior for each target wheel.
- Target simulator or simulators and the telemetry each dashboard should show.
- Dashboard design preferences and how the finished dashboards will be shared.

## Research starting point

See [the reference index](docs/REFERENCES.md). The local sample archive is kept in the ignored `references/` directory; its filename mentions CS KS PRO.

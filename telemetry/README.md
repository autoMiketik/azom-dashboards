# Telemetry catalogs

## SimHub dashboard property map

Search [simhub.csv](simhub.csv) first when choosing dashboard bindings. It contains shared `DataCorePlugin.GameData` fields from AZOM's channel catalog and selected `DataCorePlugin.Computed` fuel metrics. Search by property name, label, or AZOM channel URL. Multiple URLs for one property are separated by `|` and can have different encodings or resolver behavior.

| Column | Meaning |
| --- | --- |
| `simhub_property` | Exact source-listed SimHub property path. |
| `kind`, `label` | Property family and search label. |
| `azom_channel_urls` | Default associations listed in AZOM. A blank means this source supplies no default association for the property. |
| `iracing_sdk_fallback_candidate` | Raw SDK field to investigate if the shared property is unsuitable. Check its scaling and meaning in the target car before using it. |
| `source` | Evidence for the property name and any default association. |
| `live_verification` | A short observation or reference to a verification note. Blank means no live check is recorded. |

The map is a source-backed starting point. Actual values depend on the game, car, session, and SimHub version. Confirm them in SimHub's **Available Properties** and check the wheel binding in AZOM. [SimHub binding guide](https://github.com/SHWotever/SimHub/wiki/Dash-Studio---Bindings)

- `azom-catalog` — [AZOM telemetry channel catalog at `71985a0`](https://github.com/giantorth/AZOM/blob/71985a0f4eb7e551d665df2e2676997b6b2f8eca/Data/Telemetry.json).
- `rracingdash-fuel` — [rracingDash configuration using SimHub fuel calculations](https://github.com/chornyak/rracingDash/blob/main/SimHub/rracingDash_SimHubMapping.shsds).

## iRacing SDK telemetry catalog

Open [iracing.csv](iracing.csv) in a spreadsheet to filter the SDK fields for main dashboards and popups. The catalog combines the 2015 live data appendix, the pyirsdk variable list, and every field in the headers of five iRacing recordings. It covers driving, timing, fuel, tyres, session status, and in-car adjustments. The field list can grow as we see more cars and builds.

| Column | Meaning |
| --- | --- |
| `sdk_field` | Exact iRacing variable name. |
| `type`, `unit`, `element_count` | Metadata from recording headers when available, with the appendix used as a fallback for type and unit. A pipe separates values that differed among recordings. Blank means unspecified or unavailable in the source. |
| `metadata_basis` | Source of the displayed metadata. Rows with only a name from pyirsdk have no metadata basis. |
| `appendix_2015_live`, `appendix_2015_disk` | Published historical availability. `1` means listed as available, `0` means listed as unavailable, and blank means the field is absent from the appendix. |
| `sources` | Pipe separated source IDs from the list below. A recording ID confirms that its file header contains the field. |
| `simhub_property` | Exact SimHub property path once verified. |

Use the [live lookup checklist](../docs/IRACING_TELEMETRY.md) to confirm a SimHub path and how the value behaves before binding it to a dashboard. For new cars, [irTelemetryExplorer](https://svappslab.com/iRacing/TelemetryExplorer/) can export field metadata from a live session or `.ibt` file as CSV. Match by `sdk_field` and log the car, session, and source for new observations. Session YAML and plugin-defined SimHub properties are additional data sources to catalog as needed. Recorded fields alone cannot establish live availability.

## Sources

- `appendix-2015` — [iRacing Appendix A, Live data list](https://us.v-cdn.net/6034148/uploads/8DD84H30FIC8/telemetry-11-23-15.pdf).
- `pyirsdk` — [pyirsdk variables at `1abbd64`](https://github.com/kutu/pyirsdk/blob/1abbd64dffdc74377c215ffc783a0458bd81e614/vars.txt).
- `mustang-gt4` — [Ford Mustang GT4 at Interlagos, August 2026](https://github.com/racedirector/iracing.rs/blob/0e0facbd79d5b33335d5047d787fc443d2abb92a/test-data/ibt/fordmustanggt4_interlagos%20gp%202026-08-01%2011-24-51.ibt).
- `audi-gt3`, `mini-stock`, `ray-ff1600` — Audi R8 LMS Evo II GT3 at Spa, Mini Stock at Mount Washington, and Ray FF1600 at Road Atlanta. [iRacingTelemetrySDK recording fixtures at `9ae151b`](https://github.com/SVappsLAB/iRacingTelemetrySDK/tree/9ae151b8b1acbd8b3a3eb4a69e15f8e83a5423e3/Sdk/tests/SmokeTests/data/ibt).
- `formula-ir04` — [Formula iR-04 at Tsukuba, January 2024](https://github.com/SVappsLAB/iRacingTelemetrySDK/blob/9ae151b8b1acbd8b3a3eb4a69e15f8e83a5423e3/Samples/data/formulair04_tsukuba%202kfull%202024-01-09%2017-26-10.ibt).

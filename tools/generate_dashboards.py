#!/usr/bin/env python3
"""Generate editable MOZA CS Pro / KS Pro Dash Studio dashboards."""

from __future__ import annotations

import copy
import json
import time
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "references/reference-dashboard.zip"
EDITABLE = ROOT / "dashboards/editable"
EXPORTS = ROOT / "dashboards/exports"
WIDTH, HEIGHT = 780, 248
BG = "#0D1117"
WHITE = "#F4F7FB"
MUTED = "#AEBBCA"
RULE = "#34404D"

SETTINGS = [
    ("abs", "ABS", "ABSLevel", "#10292B", "#67C8C1", "—"),
    ("brake-bias", "BRAKE BIAS", "BrakeBias", "#322615", "#E8B760", "—"),
    ("traction-control", "TRACTION CONTROL", "TCLevel", "#29213A", "#B5A1EC", "—"),
    ("engine-map", "ENGINE MAP", "ECUMap", "#172740", "#7DA8EA", "—"),
    ("engine-braking", "ENGINE BRAKING", "EngineBrake", "#342129", "#E59BAA", "—"),
    ("tc-2", "TC 2", "TC_B", "#272D18", "#B6C77B", "—"),
]


def color(value: str) -> dict:
    return {"color": value, "type": "SOLID"}


def binding(url: str, formatter: str = "") -> dict:
    methods = [f'Telemetry.get("{url}").value']
    if formatter:
        methods.append(formatter)
    return {"text.text": {"methods": methods, "type": "METHOD_CHAINING"}}


def js_number(decimals: int = 0, suffix: str = "") -> str:
    return (
        "((v)=>{if(v===undefined||v===null)return '—';const n=Number(v);"
        f"return Number.isFinite(n)?n.toFixed({decimals})+'{suffix}':'—';}})(_result)"
    )


def js_time() -> str:
    return "((v)=>{const n=Number(v);if(!Number.isFinite(n)||n<0)return '--:--.---';const m=Math.floor(n/60),whole=Math.floor(n%60),ms=Math.floor((n%1)*1000);return String(m)+':'+String(whole).padStart(2,'0')+'.'+String(ms).padStart(3,'0');})(_result)"


def js_delta() -> str:
    return "((v)=>{const n=Number(v);if(!Number.isFinite(n))return '—';return (n<0?'−':n>0?'+':'')+Math.abs(n).toFixed(2)+' s';})(_result)"


def load_templates() -> tuple[dict, dict, dict]:
    with zipfile.ZipFile(SAMPLE) as archive:
        path = next(name for name in archive.namelist() if name.endswith(".mzdash"))
        root = json.loads(archive.read(path))
    screen = copy.deepcopy(root["children"][0])
    templates = {}

    def visit(node):
        if node.get("type") in ("Text.qml", "Rectangle.qml"):
            templates.setdefault(node["type"], copy.deepcopy(node))
        for child in node.get("children", []):
            visit(child)

    visit(root)
    return root, screen, templates


ROOT_TEMPLATE, SCREEN_TEMPLATE, WIDGETS = load_templates()


def widget(kind: str, name: str, x: float, y: float, w: float, h: float,
           text: str = "", size: int = 20, fg: str = WHITE,
           bg: str = "#00000000", weight: int = 700, align: str = "AlignCenter",
           url: str | None = None, formatter: str = "") -> dict:
    node = copy.deepcopy(WIDGETS[kind])
    node["id"] = 0
    node["name"] = name
    node["general"].update(x=x, y=y, width=w, height=h, backgroundColor=color(bg),
                           borderColor=color("#00000000"), borderWidth=0,
                           borderRadius=0, visible=True, locked=False)
    node["children"] = []
    node["actions"] = {}
    node["binding"] = {}
    if kind == "Text.qml":
        node["text"].update(text=text, fontColor=color(fg), fontFamily="Manrope3",
                            fontSize=size, fontWeight=weight,
                            horizontalAlignment=align, verticalAlignment="AlignCenter",
                            wrapText=False)
        node["textEffect"] = {"shadowBlur": 0, "shadowColor": color("#00000000"),
                              "shadowDepth": 0, "shadowDirection": 0}
        if url:
            node["binding"] = binding(url, formatter)
    return node


def rect(name: str, x: float, y: float, w: float, h: float, fill: str) -> dict:
    return widget("Rectangle.qml", name, x, y, w, h, bg=fill)


def text(name: str, value: str, x: float, y: float, w: float, h: float,
         size: int, fg: str = WHITE, weight: int = 700, align: str = "AlignCenter",
         url: str | None = None, formatter: str = "") -> dict:
    return widget("Text.qml", name, x, y, w, h, value, size, fg, weight=weight,
                  align=align, url=url, formatter=formatter)


def make_dashboard(name: str, children: list[dict], background: str = BG) -> dict:
    root = copy.deepcopy(ROOT_TEMPLATE)
    screen = copy.deepcopy(SCREEN_TEMPLATE)
    root.update(name=name, id=0, lastModified=int(time.time()), children=[screen])
    root["general"].update(width=WIDTH, height=HEIGHT, x=0, y=0,
                           backgroundColor=color(background))
    root["window"]["GUID"] = "{" + str(uuid.uuid4()) + "}"
    screen.update(name=name, id=1, children=children)
    screen["general"].update(width=WIDTH, height=HEIGHT, x=0, y=0,
                             backgroundColor=color(background))
    next_id = 2
    for item in children:
        item["id"] = next_id
        next_id += 1
    return root


def race() -> dict:
    e = [
        text("Position", "P—", 20, 4, 100, 34, 25, align="AlignLeft",
             url="v1/gameData/CurrentPos", formatter="((v)=>{const n=Number(v);return Number.isFinite(n)&&n>=0?'P'+n:'P—';})(_result)"),
        text("Session time", "--:--", 580, 4, 180, 34, 25, align="AlignRight",
             url="v1/gameData/SessionTimeLeft", formatter=js_time()),
        rect("Timing divider", 258, 55, 1, 166, RULE),
        rect("Driving divider", 555, 55, 1, 166, RULE),
    ]
    left = [
        ("CURRENT LAP", "CurrentLapTime", 58, 30),
        ("LAST LAP", "LastLapTime", 113, 28),
        ("BEST LAP", "BestLapTime", 168, 28),
    ]
    for label, prop, y, size in left:
        e.append(text(label + " label", label, 20, y, 220, 22, 15, MUTED,
                      align="AlignLeft", weight=700))
        e.append(text(label, "--:--.---", 20, y + 19, 220, 34, size,
                      align="AlignLeft", url="v1/gameData/" + prop, formatter=js_time()))
    e.extend([
        text("Speed", "—", 280, 55, 250, 46, 36,
             url="v1/gameData/SpeedKmh", formatter=js_number()),
        text("Speed unit", "km/h", 476, 62, 65, 30, 16, MUTED, align="AlignLeft"),
        text("Gear", "N", 300, 97, 210, 102, 94,
             url="v1/gameData/Gear",
             formatter="((n)=>{const v=Number(n);if(!Number.isFinite(v))return '—';if(v===0)return 'N';if(v===-1)return 'R';return String(Math.abs(v));})(_result)"),
        text("Delta label", "Δ VS SESSION BEST", 300, 195, 210, 21, 15, MUTED),
    ])
    gear = next(item for item in e if item.get("name") == "Gear")
    gear["binding"]["text.fontColor.color"] = {
        "methods": [
            'Telemetry.get("v1/gameData/CarSettings_RPMShiftLight2").value',
            "((v)=>v===true||Number(v)>0?'#FF5967':'#F4F7FB')(_result)",
        ],
        "type": "METHOD_CHAINING",
    }
    delta = text("Live delta", "—", 290, 214, 230, 30, 30,
                 url="v1/gameData/GAP", formatter=js_delta())
    delta["binding"]["text.fontColor.color"] = {
        "methods": [
            'Telemetry.get("v1/gameData/GAP").value',
            "((v)=>{const n=Number(v);if(!Number.isFinite(n))return '#F4F7FB';return n<0?'#71E6AD':n>0?'#FF8994':'#F4F7FB';})(_result)",
        ],
        "type": "METHOD_CHAINING",
    }
    e.append(delta)
    right = [
        ("FUEL LEFT", "Fuel", 58, 30, 1, " L"),
        ("FUEL PER LAP", "FuelConsumeLap", 113, 28, 2, " L/lap"),
        ("EST. FUEL LAPS", "FuelLaps", 168, 28, 1, " laps"),
    ]
    for label, prop, y, size, digits, suffix in right:
        e.append(text(label + " label", label, 570, y, 190, 22, 15, MUTED,
                      align="AlignRight", weight=700))
        e.append(text(label, "—", 570, y + 19, 190, 34, size,
                      align="AlignRight", url="v1/gameData/" + prop,
                      formatter=js_number(digits, suffix)))
    return make_dashboard("MOZA Race", e)


def settings() -> dict:
    e = []
    xs = [24, 270, 516]
    ys = [20, 134]
    for index, (slug, label, prop, _bg, accent, _fallback) in enumerate(SETTINGS):
        row, col = divmod(index, 3)
        x, y = xs[col], ys[row]
        is_bias = slug == "brake-bias"
        invalid = "!Number.isFinite(n)" if is_bias else "!Number.isFinite(n)||n<0"
        value = "Math.abs(n)<=1?n*100:n" if is_bias else "n"
        decimals = 1 if is_bias else 0
        suffix = "+'%'" if is_bias else ""
        e.append(text(label + " label", label, x, y, 240, 30, 18, MUTED))
        e.append(text(label + " value", "—", x, y + 28, 240, 66, 48,
                      url="v1/gameData/" + prop,
                      formatter=f"((v)=>{{if(v===undefined||v===null)return '—';const n=Number(v);if({invalid})return '—';return ({value}).toFixed({decimals}){suffix};}})(_result)"))
        e.append(rect(label + " accent", x + 98, y + 92, 44, 3, accent))
    e.extend([rect("Vertical divider 1", 264, 12, 1, 222, RULE),
              rect("Vertical divider 2", 510, 12, 1, 222, RULE),
              rect("Horizontal divider", 20, 125, 740, 1, RULE)])
    return make_dashboard("MOZA Settings", e)


def popup(record: tuple) -> dict:
    slug, label, prop, background, accent, _fallback = record
    is_bias = slug == "brake-bias"
    invalid = "!Number.isFinite(n)" if is_bias else "!Number.isFinite(n)||n<0"
    value = "Math.abs(n)<=1?n*100:n" if is_bias else "n"
    decimals = 1 if is_bias else 0
    suffix = "+'%'" if is_bias else ""
    e = [rect("Popup accent", 0, 0, WIDTH, 4, accent),
         text("Popup setting", label, 60, 44, 660, 34, 24, MUTED),
         text("Popup value", "—", 80, 93, 620, 118, 92,
              url="v1/gameData/" + prop,
              formatter=f"((v)=>{{if(v===undefined||v===null)return '—';const n=Number(v);if({invalid})return '—';return ({value}).toFixed({decimals}){suffix};}})(_result)")]
    return make_dashboard("MOZA Popup " + label.title(), e, background)


def main() -> None:
    EDITABLE.mkdir(parents=True, exist_ok=True)
    EXPORTS.mkdir(parents=True, exist_ok=True)
    docs = [("01-race.mzdash", race()), ("02-settings.mzdash", settings())]
    docs += [(f"{index + 3:02d}-popup-{record[0]}.mzdash", popup(record))
             for index, record in enumerate(SETTINGS)]
    for filename, content in docs:
        data = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
        (EDITABLE / filename).write_text(data, encoding="utf-8")
        (EXPORTS / filename).write_text(data, encoding="utf-8")
    with zipfile.ZipFile(ROOT / "dashboards/MOZA-CS-KS-Pro-Dashboards.zip", "w",
                         compression=zipfile.ZIP_DEFLATED) as archive:
        for filename, _ in docs:
            archive.write(EXPORTS / filename, arcname=filename)
        archive.write(ROOT / "dashboards/INSTALL.md", arcname="README.md")
        archive.write(ROOT / "dashboards/bindings.csv", arcname="bindings.csv")
        archive.write(ROOT / "dashboards/controller/controller.json",
                      arcname="controller/controller.json")
        archive.write(ROOT / "dashboards/controller/dashboard_controller.py",
                      arcname="controller/dashboard_controller.py")
        archive.write(ROOT / "dashboards/controller/run_controller.bat",
                      arcname="controller/run_controller.bat")
        archive.write(ROOT / "docs/mockups/dashboard-preview.png",
                      arcname="dashboard-preview.png")
    print(f"Generated {len(docs)} dashboards in {EDITABLE} and {EXPORTS}")


if __name__ == "__main__":
    main()

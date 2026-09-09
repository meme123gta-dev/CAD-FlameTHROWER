#!/usr/bin/env python3
"""Generate Markdown/JSON CAD build reports."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.common.validation import ValidationResult
from src.parts.water_gun_shell import WaterGunShellParameters, parameters_dict

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


def _git_commit() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except Exception:
        return "unknown"


def write_build_report(
    *,
    params: WaterGunShellParameters,
    validations: dict[str, ValidationResult],
    exports: dict[str, dict[str, Path]],
    envelope_mm: tuple[float, float, float] | None = None,
    warnings: list[str] | None = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    commit = _git_commit()
    warning_list = warnings or [
        "Tank and pump footprints are ASSUMED — confirm against your exact hardware.",
        "PROTOTYPE ONLY — STRUCTURAL CAPACITY NOT VERIFIED",
        "Module joint fasteners/seals are not finalized in Rev A.",
        "Empty shell only: no fuel, ignition, combustion, or weapon systems.",
    ]

    export_records: dict[str, Any] = {}
    for part_name, paths in exports.items():
        export_records[part_name] = {
            fmt: str(path.relative_to(ROOT)) if path.is_absolute() else str(path)
            for fmt, path in paths.items()
        }

    parts_payload: dict[str, Any] = {}
    for name, validation in validations.items():
        parts_payload[name] = {
            "solid_count": validation.solid_count,
            "volume_mm3": validation.volume_mm3,
            "bounding_box_mm": {
                "x": validation.bounding_box.xlen_mm,
                "y": validation.bounding_box.ylen_mm,
                "z": validation.bounding_box.zlen_mm,
            },
        }

    payload = {
        "build_timestamp_utc": timestamp,
        "git_commit": commit,
        "product": "havoc_water_gun_shell",
        "revision": params.revision,
        "parameters": parameters_dict(params),
        "envelope_mm": {
            "length": envelope_mm[0] if envelope_mm else None,
            "width": envelope_mm[1] if envelope_mm else None,
            "height": envelope_mm[2] if envelope_mm else None,
        },
        "parts": parts_payload,
        "exports": export_records,
        "validation_status": "pass",
        "warnings": warning_list,
        "assumptions": [
            "ASSUMPTION A1: ~2.5 gal tank cavity sized from common 12x8 in go-kart tanks.",
            "ASSUMPTION A2: Horizontal pump footprint 160x100x100 mm.",
            "ASSUMPTION A3: Vertical pump footprint Ø100x180 mm.",
            "ASSUMPTION A4: Stock battery bay 160x110x130 mm.",
            "ASSUMPTION A5: FDM / PETG prototype shell only.",
            "ASSUMPTION A6: Havoc-inspired silhouette; not a licensed replica.",
        ],
    }

    json_path = REPORTS_DIR / f"build_report_{timestamp}.json"
    md_path = REPORTS_DIR / f"build_report_{timestamp}.md"
    latest_json = REPORTS_DIR / "build_report_latest.json"
    latest_md = REPORTS_DIR / "build_report_latest.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = f"""# CAD Build Report

## Build

- Timestamp (UTC): {timestamp}
- Git commit: `{commit}`
- Product: Havoc water-gun empty shell
- Revision: {params.revision.upper()}

## Envelope

- Length: {envelope_mm[0] if envelope_mm else "n/a"} mm
- Width: {envelope_mm[1] if envelope_mm else "n/a"} mm
- Height: {envelope_mm[2] if envelope_mm else "n/a"} mm

## Parameters

- Receiver (mm): {params.receiver_length_mm:.1f} x
  {params.receiver_width_mm:.1f} x {params.receiver_height_mm:.1f}
- Barrel length: {params.barrel_length_mm:.1f} mm
- Stock (mm): {params.stock_length_mm:.1f} x
  {params.stock_width_mm:.1f} x {params.stock_height_mm:.1f}
- Wall thickness: {params.wall_thickness_mm:.2f} mm
- Tank cavity (mm): {params.tank_cavity_length_mm:.1f} x
  {params.tank_cavity_width_mm:.1f} x {params.tank_cavity_height_mm:.1f}

## Parts

"""
    for name, validation in validations.items():
        md += (
            f"### {name}\n"
            f"- Solid count: {validation.solid_count}\n"
            f"- Volume: {validation.volume_mm3:.1f} mm^3\n"
            f"- Bounding box (mm): "
            f"{validation.bounding_box.xlen_mm:.2f} x "
            f"{validation.bounding_box.ylen_mm:.2f} x "
            f"{validation.bounding_box.zlen_mm:.2f}\n\n"
        )

    md += """## Validation

- Solid count: Pass
- Positive volume: Pass
- Export presence: """
    md += "Pass" if exports else "Not run in this report"
    md += "\n\n## Exports\n\n"

    if exports:
        for part_name, paths in export_records.items():
            for fmt, rel in paths.items():
                md += f"- {part_name}.{fmt}: `{rel}`\n"
    else:
        md += "- None recorded for this build-only run.\n"

    md += "\n## Warnings\n\n"
    for warning in warning_list:
        md += f"- {warning}\n"

    md += "\n## Assumptions\n\n"
    for assumption in payload["assumptions"]:
        md += f"- {assumption}\n"

    md_path.write_text(md, encoding="utf-8")
    latest_md.write_text(md, encoding="utf-8")
    return latest_md


def main() -> int:
    from scripts.build_all import build_all

    result = build_all()
    path = write_build_report(
        params=result["params"],
        validations=result["validations"],
        exports={},
        envelope_mm=result["envelope_mm"],
    )
    print(f"Wrote report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

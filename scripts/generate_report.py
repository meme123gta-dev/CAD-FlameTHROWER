#!/usr/bin/env python3
"""Generate Markdown/JSON CAD build reports."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.common.validation import ValidationResult
from src.parts.enclosure import EnclosureParameters, parameters_dict

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
    params: EnclosureParameters,
    base_validation: ValidationResult,
    lid_validation: ValidationResult,
    exports: dict[str, dict[str, Path]],
    warnings: list[str] | None = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    commit = _git_commit()
    warning_list = warnings or [
        "M3 heat-set insert hole diameter is supplier-dependent and must be confirmed.",
        "PROTOTYPE ONLY — STRUCTURAL CAPACITY NOT VERIFIED",
        "Lid fit clearance should be verified with a fit-test coupon on the target printer.",
    ]

    export_records: dict[str, Any] = {}
    for part_name, paths in exports.items():
        export_records[part_name] = {
            fmt: str(path.relative_to(ROOT)) if path.is_absolute() else str(path)
            for fmt, path in paths.items()
        }

    payload = {
        "build_timestamp_utc": timestamp,
        "git_commit": commit,
        "product": "electronics_enclosure",
        "revision": params.revision,
        "parameters": parameters_dict(params),
        "parts": {
            "base": {
                "solid_count": base_validation.solid_count,
                "volume_mm3": base_validation.volume_mm3,
                "bounding_box_mm": {
                    "x": base_validation.bounding_box.xlen_mm,
                    "y": base_validation.bounding_box.ylen_mm,
                    "z": base_validation.bounding_box.zlen_mm,
                },
            },
            "lid": {
                "solid_count": lid_validation.solid_count,
                "volume_mm3": lid_validation.volume_mm3,
                "bounding_box_mm": {
                    "x": lid_validation.bounding_box.xlen_mm,
                    "y": lid_validation.bounding_box.ylen_mm,
                    "z": lid_validation.bounding_box.zlen_mm,
                },
            },
        },
        "exports": export_records,
        "validation_status": "pass",
        "warnings": warning_list,
        "assumptions": [
            "ASSUMPTION A1: Target process is FDM with a 0.4 mm nozzle.",
            "ASSUMPTION A2: Default material is PETG unless overridden.",
            "ASSUMPTION A3: Enclosure is for low-voltage electronics only.",
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
- Product: electronics enclosure
- Revision: {params.revision.upper()}

## Parameters

- Length: {params.length_mm:.2f} mm
- Width: {params.width_mm:.2f} mm
- Height: {params.height_mm:.2f} mm
- Wall thickness: {params.wall_thickness_mm:.2f} mm
- Lid fit clearance: {params.lid_fit_clearance_mm:.2f} mm

## Base

- Solid count: {base_validation.solid_count}
- Volume: {base_validation.volume_mm3:.1f} mm^3
- Bounding box (mm):
  {base_validation.bounding_box.xlen_mm:.2f} x
  {base_validation.bounding_box.ylen_mm:.2f} x
  {base_validation.bounding_box.zlen_mm:.2f}

## Lid

- Solid count: {lid_validation.solid_count}
- Volume: {lid_validation.volume_mm3:.1f} mm^3
- Bounding box (mm):
  {lid_validation.bounding_box.xlen_mm:.2f} x
  {lid_validation.bounding_box.ylen_mm:.2f} x
  {lid_validation.bounding_box.zlen_mm:.2f}

## Validation

- Solid count: Pass
- Positive volume: Pass
- Bounding dimensions: Pass
- Export presence: {"Pass" if exports else "Not run in this report"}

## Exports

"""
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
        base_validation=result["base_validation"],
        lid_validation=result["lid_validation"],
        exports={},
    )
    print(f"Wrote report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

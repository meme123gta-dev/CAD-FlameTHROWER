#!/usr/bin/env python3
"""Build all sample parts, validate geometry, and write a build report."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_report import write_build_report  # noqa: E402
from src.common.validation import validate_model  # noqa: E402
from src.parts.enclosure import (  # noqa: E402
    EnclosureParameters,
    build_base,
    build_lid,
    parameters_dict,
)


def build_all(params: EnclosureParameters | None = None) -> dict:
    params = params or EnclosureParameters()
    base = build_base(params)
    lid = build_lid(params)

    base_result = validate_model(
        base,
        expected_solid_count=1,
        expected_bbox_mm=(
            params.length_mm,
            params.width_mm,
            params.height_mm + params.alignment_pin_height_mm,
        ),
        bbox_tolerance_mm=0.2,
    )
    lid_result = validate_model(
        lid,
        expected_solid_count=1,
        expected_bbox_mm=(
            params.length_mm,
            params.width_mm,
            params.lid_thickness_mm + params.lid_lip_height_mm,
        ),
        bbox_tolerance_mm=0.2,
    )

    return {
        "params": params,
        "parameters": parameters_dict(params),
        "base": base,
        "lid": lid,
        "base_validation": base_result,
        "lid_validation": lid_result,
    }


def main() -> int:
    result = build_all()
    report_path = write_build_report(
        params=result["params"],
        base_validation=result["base_validation"],
        lid_validation=result["lid_validation"],
        exports={},
    )
    print("Build succeeded.")
    print(f"Base volume: {result['base_validation'].volume_mm3:.1f} mm^3")
    print(f"Lid volume: {result['lid_validation'].volume_mm3:.1f} mm^3")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

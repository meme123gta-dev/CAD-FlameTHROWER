#!/usr/bin/env python3
"""Run geometry validation for all sample parts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_all import build_all  # noqa: E402
from src.common.validation import assert_within_envelope, validate_model  # noqa: E402
from src.parts.enclosure import EnclosureParameters, validate_parameters  # noqa: E402


def main() -> int:
    params = EnclosureParameters()
    validate_parameters(params)
    result = build_all(params)

    assert_within_envelope(
        result["base"],
        max_length_mm=params.length_mm + 0.01,
        max_width_mm=params.width_mm + 0.01,
        max_height_mm=params.height_mm + params.alignment_pin_height_mm + 0.01,
    )
    assert_within_envelope(
        result["lid"],
        max_length_mm=params.length_mm + 0.01,
        max_width_mm=params.width_mm + 0.01,
        max_height_mm=params.lid_thickness_mm + params.lid_lip_height_mm + 0.01,
    )

    validate_model(result["base"], expected_solid_count=1)
    validate_model(result["lid"], expected_solid_count=1)

    print("Validation passed.")
    print(f"Base solids: {result['base_validation'].solid_count}")
    print(f"Lid solids: {result['lid_validation'].solid_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

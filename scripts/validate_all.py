#!/usr/bin/env python3
"""Run geometry validation for the water-gun empty shell."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_all import build_all  # noqa: E402
from src.common.validation import assert_within_envelope  # noqa: E402
from src.parts.water_gun_shell import (  # noqa: E402
    WaterGunShellParameters,
    overall_height_mm,
    overall_length_mm,
    overall_width_mm,
    validate_parameters,
)


def main() -> int:
    params = WaterGunShellParameters()
    validate_parameters(params)
    result = build_all(params)

    # Allow cosmetic pads / cheek plate outside the nominal envelope helpers.
    assert_within_envelope(
        result["full"],
        max_length_mm=overall_length_mm(params) + 40.0,
        max_width_mm=overall_width_mm(params) + 40.0,
        max_height_mm=overall_height_mm(params) + 20.0,
    )

    for name, validation in result["validations"].items():
        if validation.solid_count != 1:
            raise SystemExit(f"{name} failed solid-count validation")
        print(f"{name}: solids={validation.solid_count} vol={validation.volume_mm3:.1f}")

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

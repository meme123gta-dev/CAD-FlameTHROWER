#!/usr/bin/env python3
"""Build all primary parts, validate geometry, and write a build report."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_report import write_build_report  # noqa: E402
from src.common.validation import validate_model  # noqa: E402
from src.parts.water_gun_shell import (  # noqa: E402
    WaterGunShellParameters,
    build_barrel,
    build_full_shell,
    build_printable_halves,
    build_receiver,
    build_stock,
    overall_height_mm,
    overall_length_mm,
    overall_width_mm,
    parameters_dict,
)


def build_all(params: WaterGunShellParameters | None = None) -> dict:
    params = params or WaterGunShellParameters()

    receiver = build_receiver(params)
    barrel = build_barrel(params)
    stock = build_stock(params)
    full = build_full_shell(params)

    validations = {
        "receiver": validate_model(receiver, expected_solid_count=1, min_volume_mm3=100.0),
        "barrel": validate_model(barrel, expected_solid_count=1, min_volume_mm3=100.0),
        "stock": validate_model(stock, expected_solid_count=1, min_volume_mm3=100.0),
        "full": validate_model(full, expected_solid_count=1, min_volume_mm3=1000.0),
    }

    halves: dict[str, object] = {}
    for module in ("barrel", "receiver", "stock"):
        module_halves = build_printable_halves(module, params)
        for side, solid in module_halves.items():
            key = f"{module}_{side}"
            halves[key] = solid
            validations[key] = validate_model(
                solid, expected_solid_count=1, min_volume_mm3=50.0
            )

    return {
        "params": params,
        "parameters": parameters_dict(params),
        "receiver": receiver,
        "barrel": barrel,
        "stock": stock,
        "full": full,
        "halves": halves,
        "validations": validations,
        "envelope_mm": (
            overall_length_mm(params),
            overall_width_mm(params),
            overall_height_mm(params),
        ),
    }


def main() -> int:
    result = build_all()
    report_path = write_build_report(
        params=result["params"],
        validations=result["validations"],
        exports={},
        envelope_mm=result["envelope_mm"],
    )
    print("Build succeeded.")
    for name, validation in result["validations"].items():
        print(f"  {name}: volume={validation.volume_mm3:.1f} mm^3")
    print(
        "Envelope (mm): "
        f"{result['envelope_mm'][0]:.1f} x "
        f"{result['envelope_mm'][1]:.1f} x "
        f"{result['envelope_mm'][2]:.1f}"
    )
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

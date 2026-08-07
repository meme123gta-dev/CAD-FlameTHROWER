#!/usr/bin/env python3
"""Export Amazon hardware reference solids (tank + motor) for 3D design import."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.parts.hardware_motor import (  # noqa: E402
    MotorParameters,
    export_motor,
)
from src.parts.hardware_motor import (
    parameters_dict as motor_parameters_dict,
)
from src.parts.hardware_tank import (  # noqa: E402
    TankParameters,
    export_tank,
)
from src.parts.hardware_tank import (
    parameters_dict as tank_parameters_dict,
)


def main() -> int:
    tank_params = TankParameters()
    motor_params = MotorParameters()

    print("Exporting hardware reference solids...")
    tank_paths = export_tank(tank_params, stl_quality="normal")
    motor_paths = export_motor(motor_params, stl_quality="normal")

    tank_meta = tank_parameters_dict(tank_params)
    motor_meta = motor_parameters_dict(motor_params)

    print(
        f"Tank {tank_meta['asin']}: "
        f"Ø{tank_params.outer_diameter_mm:.1f} x {tank_params.length_mm:.1f} mm"
    )
    for fmt, path in tank_paths.items():
        print(f"  tank.{fmt}: {path}")

    print(
        f"Motor {motor_meta['asin']} {motor_meta['model_number']}: "
        f"{motor_params.overall_length_mm:.0f}x"
        f"{motor_params.overall_width_mm:.0f}x"
        f"{motor_params.overall_height_mm:.0f} mm"
    )
    print("  PICKUP = AIR INLET (toward motor); OUTPUT = AIR OUTLET (top)")
    for fmt, path in motor_paths.items():
        print(f"  motor.{fmt}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

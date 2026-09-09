"""Tests for Amazon hardware reference solids (tank + motor)."""

from __future__ import annotations

from src.common.validation import measure_bounding_box, validate_model
from src.parts.hardware_motor import (
    ASIN as MOTOR_ASIN,
)
from src.parts.hardware_motor import (
    MotorParameters,
    build_motor,
)
from src.parts.hardware_motor import (
    parameters_dict as motor_parameters_dict,
)
from src.parts.hardware_tank import (
    ASIN as TANK_ASIN,
)
from src.parts.hardware_tank import (
    TankParameters,
    build_tank,
)
from src.parts.hardware_tank import (
    parameters_dict as tank_parameters_dict,
)


def test_tank_asin_and_exact_size():
    params = TankParameters()
    assert TANK_ASIN == "B0BSDYNDQP"
    assert abs(params.outer_diameter_mm - 76.2) < 1e-6
    assert abs(params.length_mm - 254.0) < 1e-6
    bbox = measure_bounding_box(build_tank(params))
    assert abs(bbox.xlen_mm - params.length_mm) < 1.0
    # Caps add ~2 mm to diameter; outlet boss adds on +Y.
    assert bbox.ylen_mm >= params.outer_diameter_mm - 0.5
    assert bbox.zlen_mm >= params.outer_diameter_mm - 0.5


def test_tank_is_single_solid():
    result = validate_model(build_tank(), expected_solid_count=1, min_volume_mm3=100.0)
    assert result.volume_mm3 > 0


def test_tank_port_role_documented():
    roles = tank_parameters_dict(TankParameters())["port_roles"]
    assert "center_outlet" in roles


def test_motor_asin_and_envelope():
    params = MotorParameters()
    assert MOTOR_ASIN == "B07NYZ2CGK"
    assert params.overall_length_mm == 90.0
    assert params.overall_width_mm == 44.0
    assert params.overall_height_mm == 110.0
    assert params.port_od_mm == 8.0
    bbox = measure_bounding_box(build_motor(params))
    # Model should stay near the seller envelope (plate/ports may slightly exceed).
    assert bbox.xlen_mm <= params.overall_length_mm + 25.0
    assert bbox.ylen_mm <= params.overall_width_mm + 20.0
    assert bbox.zlen_mm <= params.overall_height_mm + 25.0


def test_motor_is_single_solid():
    result = validate_model(build_motor(), expected_solid_count=1, min_volume_mm3=100.0)
    assert result.volume_mm3 > 0


def test_motor_pickup_and_output_roles():
    roles = motor_parameters_dict(MotorParameters())["port_roles"]
    assert "PICKUP" in roles["pickup_air_inlet"]["role"]
    assert "OUTPUT" in roles["output_air_outlet"]["role"]
    assert "INLET" in roles["pickup_air_inlet"]["role"]
    assert "OUTLET" in roles["output_air_outlet"]["role"]

"""Clearance and packing-envelope tests for the water-gun empty shell."""

from __future__ import annotations

import pytest

from src.parts.water_gun_shell import WaterGunShellParameters, validate_parameters


def test_split_kerf_must_be_non_negative():
    params = WaterGunShellParameters(split_kerf_mm=-0.1)
    with pytest.raises(ValueError, match="split_kerf_mm"):
        validate_parameters(params)


def test_tank_clearance_expands_packing_envelope():
    params = WaterGunShellParameters()
    tank_l = params.tank_cavity_length_mm + 2 * params.tank_clearance_mm
    tank_w = params.tank_cavity_width_mm + 2 * params.tank_clearance_mm
    assert tank_l < params.receiver_length_mm - 2 * params.wall_thickness_mm
    assert tank_w < params.receiver_width_mm - 2 * params.wall_thickness_mm


def test_flange_clearance_reserved_positive_default():
    params = WaterGunShellParameters()
    assert params.flange_clearance_mm > 0
    assert params.flange_depth_mm > 0


def test_bore_smaller_than_outer_barrel():
    params = WaterGunShellParameters()
    assert params.barrel_bore_diameter_mm < params.barrel_outer_diameter_front_mm
    assert params.barrel_bore_diameter_mm < params.barrel_outer_diameter_rear_mm

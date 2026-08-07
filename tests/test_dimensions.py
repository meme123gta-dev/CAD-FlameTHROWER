"""Bounding-box and dimensional tests for the water-gun empty shell."""

from __future__ import annotations

from src.common.validation import measure_bounding_box
from src.parts.water_gun_shell import (
    WaterGunShellParameters,
    build_barrel,
    build_receiver,
    build_stock,
    overall_length_mm,
)


def test_receiver_length_matches_parameters():
    params = WaterGunShellParameters()
    bbox = measure_bounding_box(build_receiver(params))
    assert abs(bbox.xlen_mm - params.receiver_length_mm) < 0.5


def test_barrel_length_matches_parameters():
    params = WaterGunShellParameters()
    bbox = measure_bounding_box(build_barrel(params))
    assert abs(bbox.xlen_mm - params.barrel_length_mm) < 0.5


def test_stock_length_near_parameters():
    params = WaterGunShellParameters()
    bbox = measure_bounding_box(build_stock(params))
    # Butt pad can extend a few mm past stock_length.
    assert bbox.xlen_mm >= params.stock_length_mm - 0.5
    assert bbox.xlen_mm <= params.stock_length_mm + 30.0


def test_overall_length_sum():
    params = WaterGunShellParameters()
    expected = (
        params.stock_length_mm + params.receiver_length_mm + params.barrel_length_mm
    )
    assert abs(overall_length_mm(params) - expected) < 1e-6


def test_custom_barrel_length_propagates():
    params = WaterGunShellParameters(barrel_length_mm=500.0)
    bbox = measure_bounding_box(build_barrel(params))
    assert abs(bbox.xlen_mm - 500.0) < 0.5

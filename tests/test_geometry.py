"""Geometry validity tests for the Havoc water-gun empty shell."""

from __future__ import annotations

import pytest

from src.common.validation import validate_model
from src.parts.water_gun_shell import (
    WaterGunShellParameters,
    build_barrel,
    build_full_shell,
    build_printable_halves,
    build_receiver,
    build_stock,
    validate_parameters,
)
from src.variants.product_variants import compact_shell, get_variant


def test_receiver_is_single_positive_solid():
    result = validate_model(build_receiver(), expected_solid_count=1)
    assert result.volume_mm3 > 0


def test_barrel_is_single_positive_solid():
    result = validate_model(build_barrel(), expected_solid_count=1)
    assert result.volume_mm3 > 0


def test_stock_is_single_positive_solid():
    result = validate_model(build_stock(), expected_solid_count=1)
    assert result.volume_mm3 > 0


def test_full_shell_is_single_positive_solid():
    result = validate_model(build_full_shell(), expected_solid_count=1, min_volume_mm3=1000.0)
    assert result.volume_mm3 > 0


def test_printable_halves_are_single_solids():
    for module in ("barrel", "receiver", "stock"):
        halves = build_printable_halves(module)
        for side, solid in halves.items():
            result = validate_model(solid, expected_solid_count=1, min_volume_mm3=50.0)
            assert result.volume_mm3 > 0, f"{module}_{side}"


def test_invalid_wall_thickness_rejected():
    params = WaterGunShellParameters(wall_thickness_mm=0.5)
    with pytest.raises(ValueError, match="wall_thickness_mm"):
        validate_parameters(params)


def test_tank_too_large_rejected():
    params = WaterGunShellParameters(
        tank_cavity_length_mm=500.0,
        tank_clearance_mm=10.0,
    )
    with pytest.raises(ValueError, match="tank cavity"):
        validate_parameters(params)


def test_compact_variant_builds():
    params = compact_shell()
    assert len(build_receiver(params).solids().vals()) == 1
    assert len(build_barrel(params).solids().vals()) == 1
    assert len(build_stock(params).solids().vals()) == 1


def test_p1s_segments_fit_bed():
    from src.parts.water_gun_shell import (
        _fits_printer,
        build_p1s_segments,
        p1s_parameters,
    )

    params = p1s_parameters()
    segments = build_p1s_segments(params)
    assert len(segments) >= 10
    for name, solid in segments.items():
        assert _fits_printer(solid, params), name


def test_p1s_exploded_has_multiple_solids():
    from src.parts.water_gun_shell import build_exploded_assembly, p1s_parameters

    exploded = build_exploded_assembly(p1s_parameters())
    assert len(exploded.solids().vals()) >= 10


def test_get_variant_unknown():
    with pytest.raises(KeyError):
        get_variant("not_a_real_variant")

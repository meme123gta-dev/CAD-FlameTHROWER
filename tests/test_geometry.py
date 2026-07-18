"""Geometry validity tests for the sample electronics enclosure."""

from __future__ import annotations

import pytest

from src.common.validation import validate_model
from src.parts.enclosure import EnclosureParameters, build_base, build_lid, validate_parameters


def test_base_is_single_positive_solid():
    model = build_base()
    result = validate_model(model, expected_solid_count=1)
    assert result.volume_mm3 > 0


def test_lid_is_single_positive_solid():
    model = build_lid()
    result = validate_model(model, expected_solid_count=1)
    assert result.volume_mm3 > 0


def test_invalid_wall_thickness_rejected():
    params = EnclosureParameters(wall_thickness_mm=0.5)
    with pytest.raises(ValueError, match="wall_thickness_mm"):
        validate_parameters(params)


def test_compact_variant_builds():
    params = EnclosureParameters(length_mm=120.0, width_mm=70.0, height_mm=40.0)
    base = build_base(params)
    lid = build_lid(params)
    assert len(base.solids().vals()) == 1
    assert len(lid.solids().vals()) == 1

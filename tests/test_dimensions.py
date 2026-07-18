"""Bounding-box and dimensional tests for the sample enclosure."""

from __future__ import annotations

from src.common.validation import measure_bounding_box
from src.parts.enclosure import EnclosureParameters, build_base, build_lid


def test_base_bounding_box_matches_parameters():
    params = EnclosureParameters()
    bbox = measure_bounding_box(build_base(params))

    assert abs(bbox.xlen_mm - params.length_mm) < 0.05
    assert abs(bbox.ylen_mm - params.width_mm) < 0.05
    assert abs(bbox.zlen_mm - (params.height_mm + params.alignment_pin_height_mm)) < 0.20


def test_lid_bounding_box_matches_parameters():
    params = EnclosureParameters()
    bbox = measure_bounding_box(build_lid(params))

    assert abs(bbox.xlen_mm - params.length_mm) < 0.05
    assert abs(bbox.ylen_mm - params.width_mm) < 0.05
    assert abs(bbox.zlen_mm - (params.lid_thickness_mm + params.lid_lip_height_mm)) < 0.20


def test_custom_width_propagates():
    params = EnclosureParameters(width_mm=75.0)
    bbox = measure_bounding_box(build_base(params))
    assert abs(bbox.ylen_mm - 75.0) < 0.05

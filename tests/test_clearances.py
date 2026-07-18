"""Fit and clearance related tests for lid/base mating."""

from __future__ import annotations

import pytest

from src.parts.enclosure import EnclosureParameters, build_lid, validate_parameters


def test_lid_fit_clearance_must_be_non_negative():
    params = EnclosureParameters(lid_fit_clearance_mm=-0.1)
    with pytest.raises(ValueError, match="lid_fit_clearance_mm"):
        validate_parameters(params)


def test_lid_builds_with_increased_clearance():
    params = EnclosureParameters(lid_fit_clearance_mm=0.50)
    lid = build_lid(params)
    assert len(lid.solids().vals()) == 1


def test_alignment_socket_larger_than_pin():
    params = EnclosureParameters()
    socket_diameter = (
        params.alignment_pin_diameter_mm + 2 * params.alignment_socket_clearance_mm
    )
    assert socket_diameter > params.alignment_pin_diameter_mm

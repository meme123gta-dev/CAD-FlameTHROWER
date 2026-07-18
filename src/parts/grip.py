"""
Part name: Generic ergonomic grip (placeholder)
Purpose: Reserved module for future safe ergonomic grips and handles.
Units: millimeters
Revision: A
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GripParameters:
    length_mm: float = 110.0
    diameter_mm: float = 32.0
    revision: str = "a"


def validate_parameters(params: GripParameters) -> None:
    if params.length_mm <= 0 or params.diameter_mm <= 0:
        raise ValueError("grip dimensions must be positive")


def build_part(params: GripParameters | None = None):
    """Placeholder for future grip geometry."""
    raise NotImplementedError(
        "Grip geometry is not implemented yet. Use enclosure.py for the sample part."
    )

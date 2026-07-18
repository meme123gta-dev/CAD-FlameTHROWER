"""
Part name: Generic mounting bracket (placeholder)
Purpose: Reserved module for future safe mounting brackets and fixtures.
Units: millimeters
Revision: A
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BracketParameters:
    length_mm: float = 80.0
    width_mm: float = 40.0
    thickness_mm: float = 4.0
    revision: str = "a"


def validate_parameters(params: BracketParameters) -> None:
    if params.length_mm <= 0 or params.width_mm <= 0 or params.thickness_mm <= 0:
        raise ValueError("bracket dimensions must be positive")


def build_part(params: BracketParameters | None = None):
    """Placeholder for future bracket geometry."""
    raise NotImplementedError(
        "Bracket geometry is not implemented yet. Use enclosure.py for the sample part."
    )

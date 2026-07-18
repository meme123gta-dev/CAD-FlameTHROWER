"""Standard fastener dimensions and helpers.

Hole sizes for heat-set inserts are supplier-dependent starting values.
Confirm against the specific insert datasheet before production use.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.common.constants import (
    M3_CLEARANCE_HOLE_MM,
    M3_HEAD_COUNTERBORE_DEPTH_MM,
    M3_HEAD_COUNTERBORE_MM,
    M3_HEAT_SET_INSERT_HOLE_MM,
    M3_NUT_FLAT_TO_FLAT_MM,
    M3_NUT_THICKNESS_MM,
    M4_CLEARANCE_HOLE_MM,
    M4_HEAT_SET_INSERT_HOLE_MM,
)


@dataclass(frozen=True)
class MetricScrewSpec:
    name: str
    clearance_hole_mm: float
    heat_set_insert_hole_mm: float
    head_counterbore_mm: float
    head_counterbore_depth_mm: float
    nut_flat_to_flat_mm: float | None = None
    nut_thickness_mm: float | None = None
    notes: str = "Confirm insert hole diameter with supplier datasheet."


M3 = MetricScrewSpec(
    name="M3",
    clearance_hole_mm=M3_CLEARANCE_HOLE_MM,
    heat_set_insert_hole_mm=M3_HEAT_SET_INSERT_HOLE_MM,
    head_counterbore_mm=M3_HEAD_COUNTERBORE_MM,
    head_counterbore_depth_mm=M3_HEAD_COUNTERBORE_DEPTH_MM,
    nut_flat_to_flat_mm=M3_NUT_FLAT_TO_FLAT_MM,
    nut_thickness_mm=M3_NUT_THICKNESS_MM,
)

M4 = MetricScrewSpec(
    name="M4",
    clearance_hole_mm=M4_CLEARANCE_HOLE_MM,
    heat_set_insert_hole_mm=M4_HEAT_SET_INSERT_HOLE_MM,
    head_counterbore_mm=8.0,
    head_counterbore_depth_mm=4.0,
)


def boss_outer_diameter_mm(insert_hole_mm: float, boss_wall_mm: float) -> float:
    """Return recommended cylindrical boss outer diameter for an insert hole."""
    return insert_hole_mm + 2.0 * boss_wall_mm

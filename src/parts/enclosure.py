"""
Part name: Low-voltage electronics enclosure (base + lid)
Purpose: Houses low-voltage control electronics only.
Units: millimeters
Revision: A

Coordinate system:
- Origin at the geometric center of the outer XY envelope.
- +X along length, +Y along width, +Z upward.
- Z = 0 at the exterior bottom of the base.
- Lid sits on top of the base and nests with a lip into the base cavity.

Safety:
- No fuel, ignition, combustion, pressure, or flame-related features.
- Intended only for low-voltage electronics enclosures and display mockups.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import cadquery as cq

from src.common.constants import (
    DEFAULT_BOSS_WALL_MM,
    DEFAULT_CHAMFER_MM,
    DEFAULT_FILLET_MM,
    DEFAULT_LID_FIT_CLEARANCE_MM,
    DEFAULT_MIN_WALL_MM,
    DEFAULT_STRUCTURAL_WALL_MM,
    M3_CLEARANCE_HOLE_MM,
    M3_HEAD_COUNTERBORE_DEPTH_MM,
    M3_HEAD_COUNTERBORE_MM,
    M3_HEAT_SET_INSERT_HOLE_MM,
)
from src.common.exporters import export_part_formats
from src.common.fasteners import boss_outer_diameter_mm
from src.common.validation import validate_model

PRODUCT_NAME = "electronics_enclosure"
REVISION = "a"
VARIANT = "default"


@dataclass(frozen=True)
class EnclosureParameters:
    """Parametric definition for the two-piece enclosure."""

    length_mm: float = 160.0
    width_mm: float = 90.0
    height_mm: float = 50.0
    wall_thickness_mm: float = DEFAULT_STRUCTURAL_WALL_MM
    floor_thickness_mm: float = DEFAULT_STRUCTURAL_WALL_MM
    lid_thickness_mm: float = 3.2
    corner_radius_mm: float = 6.0
    lid_fit_clearance_mm: float = DEFAULT_LID_FIT_CLEARANCE_MM
    lid_lip_height_mm: float = 4.0
    lid_lip_thickness_mm: float = 2.0

    # M3 heat-set insert bosses (supplier-dependent hole size).
    insert_hole_diameter_mm: float = M3_HEAT_SET_INSERT_HOLE_MM
    screw_clearance_diameter_mm: float = M3_CLEARANCE_HOLE_MM
    screw_counterbore_diameter_mm: float = M3_HEAD_COUNTERBORE_MM
    screw_counterbore_depth_mm: float = M3_HEAD_COUNTERBORE_DEPTH_MM
    boss_wall_mm: float = DEFAULT_BOSS_WALL_MM
    boss_height_mm: float = 10.0
    boss_inset_from_inner_mm: float = 1.0

    # Cable entry on -X wall (low-voltage cable routing only).
    cable_port_width_mm: float = 14.0
    cable_port_height_mm: float = 8.0
    cable_port_bottom_offset_mm: float = 10.0

    # Alignment features between base and lid (pin diameter must fit wall rim).
    alignment_pin_diameter_mm: float = 1.6
    alignment_pin_height_mm: float = 2.5
    alignment_socket_clearance_mm: float = 0.25

    outer_fillet_mm: float = DEFAULT_FILLET_MM
    edge_chamfer_mm: float = DEFAULT_CHAMFER_MM
    revision: str = REVISION


def validate_parameters(params: EnclosureParameters) -> None:
    """Raise ValueError when parameters are geometrically invalid."""
    if params.length_mm <= 0 or params.width_mm <= 0 or params.height_mm <= 0:
        raise ValueError("overall dimensions must be positive")

    if params.wall_thickness_mm < DEFAULT_MIN_WALL_MM:
        raise ValueError(
            f"wall_thickness_mm must be >= {DEFAULT_MIN_WALL_MM} for FDM durability"
        )

    if params.floor_thickness_mm < DEFAULT_MIN_WALL_MM:
        raise ValueError("floor_thickness_mm is too thin for the intended process")

    if params.lid_thickness_mm < DEFAULT_MIN_WALL_MM:
        raise ValueError("lid_thickness_mm is too thin for the intended process")

    if params.wall_thickness_mm * 2 >= params.width_mm:
        raise ValueError("wall thickness leaves no internal cavity in width")

    if params.wall_thickness_mm * 2 >= params.length_mm:
        raise ValueError("wall thickness leaves no internal cavity in length")

    if params.floor_thickness_mm >= params.height_mm:
        raise ValueError("floor thickness leaves no internal cavity in height")

    if params.lid_lip_height_mm <= 0:
        raise ValueError("lid_lip_height_mm must be positive")

    if params.lid_fit_clearance_mm < 0:
        raise ValueError("lid_fit_clearance_mm must be non-negative")

    inner_length = params.length_mm - 2 * params.wall_thickness_mm
    inner_width = params.width_mm - 2 * params.wall_thickness_mm
    if inner_length <= 2 * params.lid_lip_thickness_mm:
        raise ValueError("lid lip thickness does not fit in internal length")
    if inner_width <= 2 * params.lid_lip_thickness_mm:
        raise ValueError("lid lip thickness does not fit in internal width")

    boss_od = boss_outer_diameter_mm(params.insert_hole_diameter_mm, params.boss_wall_mm)
    if boss_od >= min(inner_length, inner_width):
        raise ValueError("boss outer diameter exceeds internal cavity")

    if params.cable_port_width_mm <= 0 or params.cable_port_height_mm <= 0:
        raise ValueError("cable port dimensions must be positive")

    if (
        params.cable_port_bottom_offset_mm + params.cable_port_height_mm
        >= params.height_mm - params.lid_lip_height_mm
    ):
        raise ValueError("cable port intersects the lid mating region")

    if params.corner_radius_mm < 0:
        raise ValueError("corner_radius_mm must be non-negative")

    max_corner = min(params.length_mm, params.width_mm) / 2.0 - 0.1
    if params.corner_radius_mm > max_corner:
        raise ValueError("corner_radius_mm is too large for the envelope")


def _corner_radius(params: EnclosureParameters) -> float:
    max_corner = min(params.length_mm, params.width_mm) / 2.0 - 0.1
    return min(params.corner_radius_mm, max_corner)


def _boss_centers(params: EnclosureParameters) -> list[tuple[float, float]]:
    """Return XY centers for the four corner bosses."""
    boss_od = boss_outer_diameter_mm(params.insert_hole_diameter_mm, params.boss_wall_mm)
    inset = (
        params.wall_thickness_mm
        + params.boss_inset_from_inner_mm
        + boss_od / 2.0
    )
    x = params.length_mm / 2.0 - inset
    y = params.width_mm / 2.0 - inset
    return [
        (x, y),
        (x, -y),
        (-x, y),
        (-x, -y),
    ]


def _alignment_centers(params: EnclosureParameters) -> list[tuple[float, float]]:
    """Return XY centers for two alignment pins on the top wall rim."""
    # Center pins in the wall thickness at the ±X ends so they fuse to the rim.
    x = params.length_mm / 2.0 - params.wall_thickness_mm / 2.0
    y = 0.0
    return [(x, y), (-x, y)]


def build_base(params: EnclosureParameters | None = None) -> cq.Workplane:
    """Build the enclosure base with insert bosses, cable port, and alignment pins."""
    params = params or EnclosureParameters()
    validate_parameters(params)

    corner_radius = _corner_radius(params)
    cavity_height = params.height_mm - params.floor_thickness_mm
    inner_length = params.length_mm - 2 * params.wall_thickness_mm
    inner_width = params.width_mm - 2 * params.wall_thickness_mm

    outer = (
        cq.Workplane("XY")
        .workplane(offset=params.height_mm / 2.0)
        .box(params.length_mm, params.width_mm, params.height_mm)
    )
    if corner_radius > 0:
        outer = outer.edges("|Z").fillet(corner_radius)

    cavity = (
        cq.Workplane("XY")
        .workplane(offset=params.floor_thickness_mm + cavity_height / 2.0)
        .box(inner_length, inner_width, cavity_height + 0.2)
    )
    base = outer.cut(cavity)

    boss_od = boss_outer_diameter_mm(params.insert_hole_diameter_mm, params.boss_wall_mm)
    boss_height = min(
        params.boss_height_mm,
        params.height_mm - params.floor_thickness_mm - 1.0,
    )
    # Overlap bosses into the floor so boolean fuse produces one solid.
    boss_overlap_mm = 0.2
    for x, y in _boss_centers(params):
        boss = (
            cq.Workplane("XY")
            .workplane(offset=params.floor_thickness_mm - boss_overlap_mm)
            .center(x, y)
            .circle(boss_od / 2.0)
            .extrude(boss_height + boss_overlap_mm)
        )
        base = base.union(boss)

    for x, y in _boss_centers(params):
        hole = (
            cq.Workplane("XY")
            .workplane(offset=params.floor_thickness_mm - 0.1)
            .center(x, y)
            .circle(params.insert_hole_diameter_mm / 2.0)
            .extrude(boss_height + 0.3)
        )
        base = base.cut(hole)

    # Cable-entry opening on the -X wall for low-voltage cable routing.
    port_z = (
        params.cable_port_bottom_offset_mm
        + params.cable_port_height_mm / 2.0
    )
    cable_port = (
        cq.Workplane("XY")
        .workplane(offset=port_z)
        .center(-params.length_mm / 2.0, 0)
        .box(
            params.wall_thickness_mm + 2.0,
            params.cable_port_width_mm,
            params.cable_port_height_mm,
            centered=True,
        )
    )
    base = base.cut(cable_port)

    pin_radius = params.alignment_pin_diameter_mm / 2.0
    pin_overlap_mm = 0.2
    for x, y in _alignment_centers(params):
        pin = (
            cq.Workplane("XY")
            .workplane(offset=params.height_mm - pin_overlap_mm)
            .center(x, y)
            .circle(pin_radius)
            .extrude(params.alignment_pin_height_mm + pin_overlap_mm)
        )
        base = base.union(pin)

    # Ensure a single solid after boolean operations.
    solids = base.solids().vals()
    if len(solids) > 1:
        fused = solids[0]
        for solid in solids[1:]:
            fused = fused.fuse(solid)
        base = cq.Workplane("XY").newObject([fused])

    if params.edge_chamfer_mm > 0:
        try:
            base = base.edges("<Z").chamfer(params.edge_chamfer_mm)
        except Exception:
            # Chamfer can fail on complex topology; keep the solid valid.
            pass

    return base


def build_lid(params: EnclosureParameters | None = None) -> cq.Workplane:
    """Build the removable lid with lip, screw counterbores, and alignment sockets."""
    params = params or EnclosureParameters()
    validate_parameters(params)

    corner_radius = _corner_radius(params)
    inner_length = params.length_mm - 2 * params.wall_thickness_mm
    inner_width = params.width_mm - 2 * params.wall_thickness_mm

    lid_plate = (
        cq.Workplane("XY")
        .workplane(offset=params.lid_thickness_mm / 2.0)
        .box(params.length_mm, params.width_mm, params.lid_thickness_mm)
    )
    if corner_radius > 0:
        lid_plate = lid_plate.edges("|Z").fillet(corner_radius)

    lip_outer_length = inner_length - 2 * params.lid_fit_clearance_mm
    lip_outer_width = inner_width - 2 * params.lid_fit_clearance_mm
    lip_inner_length = lip_outer_length - 2 * params.lid_lip_thickness_mm
    lip_inner_width = lip_outer_width - 2 * params.lid_lip_thickness_mm

    if lip_inner_length <= 0 or lip_inner_width <= 0:
        raise ValueError("lid lip geometry is invalid after clearance is applied")

    lip_outer = (
        cq.Workplane("XY")
        .workplane(offset=-params.lid_lip_height_mm / 2.0)
        .box(lip_outer_length, lip_outer_width, params.lid_lip_height_mm)
    )
    lip_inner = (
        cq.Workplane("XY")
        .workplane(offset=-params.lid_lip_height_mm / 2.0)
        .box(
            lip_inner_length,
            lip_inner_width,
            params.lid_lip_height_mm + 0.2,
        )
    )
    lid = lid_plate.union(lip_outer.cut(lip_inner))

    for x, y in _boss_centers(params):
        through_hole = (
            cq.Workplane("XY")
            .workplane(offset=-params.lid_lip_height_mm - 0.1)
            .center(x, y)
            .circle(params.screw_clearance_diameter_mm / 2.0)
            .extrude(params.lid_thickness_mm + params.lid_lip_height_mm + 0.2)
        )
        counterbore = (
            cq.Workplane("XY")
            .workplane(
                offset=params.lid_thickness_mm - params.screw_counterbore_depth_mm
            )
            .center(x, y)
            .circle(params.screw_counterbore_diameter_mm / 2.0)
            .extrude(params.screw_counterbore_depth_mm + 0.1)
        )
        lid = lid.cut(through_hole).cut(counterbore)

    socket_diameter = (
        params.alignment_pin_diameter_mm + 2 * params.alignment_socket_clearance_mm
    )
    for x, y in _alignment_centers(params):
        socket = (
            cq.Workplane("XY")
            .workplane(offset=-params.lid_lip_height_mm - 0.1)
            .center(x, y)
            .circle(socket_diameter / 2.0)
            .extrude(params.alignment_pin_height_mm + params.lid_lip_height_mm + 0.2)
        )
        lid = lid.cut(socket)

    if params.edge_chamfer_mm > 0:
        try:
            lid = lid.edges(">Z").chamfer(min(params.edge_chamfer_mm, 0.4))
        except Exception:
            pass

    return lid


def build_part(params: EnclosureParameters | None = None) -> cq.Workplane:
    """Compatibility helper that returns the enclosure base."""
    return build_base(params)


def parameters_dict(params: EnclosureParameters) -> dict:
    return asdict(params)


def export_enclosure(
    params: EnclosureParameters | None = None,
    *,
    stl_quality: str = "normal",
) -> dict[str, dict[str, Path]]:
    """Validate and export base + lid STEP/STL files."""
    params = params or EnclosureParameters()
    validate_parameters(params)

    base = build_base(params)
    lid = build_lid(params)

    validate_model(
        base,
        expected_solid_count=1,
        expected_bbox_mm=(
            params.length_mm,
            params.width_mm,
            params.height_mm + params.alignment_pin_height_mm,
        ),
        bbox_tolerance_mm=0.2,
    )
    validate_model(
        lid,
        expected_solid_count=1,
        expected_bbox_mm=(
            params.length_mm,
            params.width_mm,
            params.lid_thickness_mm + params.lid_lip_height_mm,
        ),
        bbox_tolerance_mm=0.2,
    )

    base_paths = export_part_formats(
        base,
        product=PRODUCT_NAME,
        part="base",
        variant=VARIANT,
        revision=params.revision,
        stl_quality=stl_quality,
    )
    lid_paths = export_part_formats(
        lid,
        product=PRODUCT_NAME,
        part="lid",
        variant=VARIANT,
        revision=params.revision,
        stl_quality=stl_quality,
    )
    return {"base": base_paths, "lid": lid_paths}


if __name__ == "__main__":
    parameters = EnclosureParameters()
    outputs = export_enclosure(parameters)
    for part_name, paths in outputs.items():
        for fmt, path in paths.items():
            print(f"{part_name}.{fmt}: {path}")

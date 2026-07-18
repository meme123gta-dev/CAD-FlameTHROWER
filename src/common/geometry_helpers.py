"""Reusable CadQuery geometry helpers for printable product parts."""

from __future__ import annotations

import cadquery as cq


def rounded_box(
    length_mm: float,
    width_mm: float,
    height_mm: float,
    corner_radius_mm: float,
    *,
    centered: bool = True,
) -> cq.Workplane:
    """Create a rectangular solid with vertical-edge fillets."""
    solid = cq.Workplane("XY").box(length_mm, width_mm, height_mm, centered=centered)
    if corner_radius_mm > 0:
        max_radius = min(length_mm, width_mm) / 2.0 - 0.05
        radius = min(corner_radius_mm, max_radius)
        if radius > 0:
            solid = solid.edges("|Z").fillet(radius)
    return solid


def shell_box(
    length_mm: float,
    width_mm: float,
    height_mm: float,
    wall_thickness_mm: float,
    corner_radius_mm: float = 0.0,
    *,
    open_face: str = "-Z",
) -> cq.Workplane:
    """Create a hollow box open on one face.

    open_face uses CadQuery face selectors such as "+Z" or "-Z".
    """
    outer = rounded_box(length_mm, width_mm, height_mm, corner_radius_mm)
    return outer.faces(open_face).shell(-wall_thickness_mm)


def cylindrical_boss(
    outer_diameter_mm: float,
    height_mm: float,
    hole_diameter_mm: float,
) -> cq.Workplane:
    """Create a cylindrical boss with a through hole."""
    if hole_diameter_mm >= outer_diameter_mm:
        raise ValueError("hole_diameter_mm must be smaller than outer_diameter_mm")

    boss = cq.Workplane("XY").circle(outer_diameter_mm / 2.0).extrude(height_mm)
    return boss.faces(">Z").workplane().hole(hole_diameter_mm)


def counterbore_at(
    workplane: cq.Workplane,
    hole_diameter_mm: float,
    counterbore_diameter_mm: float,
    counterbore_depth_mm: float,
) -> cq.Workplane:
    """Cut a counterbored hole on the current workplane selection."""
    return workplane.cboreHole(
        hole_diameter_mm,
        counterbore_diameter_mm,
        counterbore_depth_mm,
    )


def rectangular_slot(
    length_mm: float,
    width_mm: float,
    depth_mm: float,
) -> cq.Workplane:
    """Create a rectangular cutting solid for cable ports and vents."""
    return cq.Workplane("XY").box(length_mm, width_mm, depth_mm)


def alignment_pin(
    diameter_mm: float,
    height_mm: float,
) -> cq.Workplane:
    """Create a simple cylindrical alignment pin."""
    return cq.Workplane("XY").circle(diameter_mm / 2.0).extrude(height_mm)


def alignment_socket(
    diameter_mm: float,
    depth_mm: float,
) -> cq.Workplane:
    """Create a cylindrical socket cutter for alignment pins."""
    return cq.Workplane("XY").circle(diameter_mm / 2.0).extrude(depth_mm)

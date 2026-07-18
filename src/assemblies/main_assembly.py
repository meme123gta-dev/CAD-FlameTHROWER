"""
Assembly: Low-voltage electronics enclosure
Purpose: Position base and lid for fit visualization.
Units: millimeters
Revision: A

Does not include fasteners as solids. Hazardous internal systems are excluded.
"""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

from src.parts.enclosure import EnclosureParameters, build_base, build_lid


@dataclass(frozen=True)
class AssemblyParameters:
    enclosure: EnclosureParameters = EnclosureParameters()
    explode_gap_mm: float = 0.0
    revision: str = "a"


def build_assembly(params: AssemblyParameters | None = None) -> cq.Assembly:
    """Create a CadQuery assembly with base and lid in mating position."""
    params = params or AssemblyParameters()
    enclosure = params.enclosure

    base = build_base(enclosure)
    lid = build_lid(enclosure)

    lid_z = enclosure.height_mm + params.explode_gap_mm
    assembly = cq.Assembly(name="electronics_enclosure_rev_a")
    assembly.add(base, name="base", color=cq.Color(0.2, 0.2, 0.25, 1.0))
    assembly.add(
        lid,
        name="lid",
        loc=cq.Location(cq.Vector(0, 0, lid_z)),
        color=cq.Color(0.35, 0.35, 0.4, 1.0),
    )
    return assembly


def build_compound(params: AssemblyParameters | None = None) -> cq.Workplane:
    """Return a compound Workplane of base + positioned lid for simple export."""
    params = params or AssemblyParameters()
    enclosure = params.enclosure
    base = build_base(enclosure)
    lid = build_lid(enclosure).translate((0, 0, enclosure.height_mm + params.explode_gap_mm))
    return base.union(lid)


if __name__ == "__main__":
    compound = build_compound()
    print(f"Assembly solid count: {len(compound.solids().vals())}")

"""
Assembly: Havoc-inspired theatrical water-gun empty shell
Purpose: Position barrel, receiver, and stock for fit visualization.
Units: millimeters
Revision: A

Hazardous internal systems are excluded. Modules are empty shells only.
"""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

from src.parts.water_gun_shell import (
    WaterGunShellParameters,
    build_barrel,
    build_full_shell,
    build_receiver,
    build_stock,
)


@dataclass(frozen=True)
class AssemblyParameters:
    shell: WaterGunShellParameters = WaterGunShellParameters()
    revision: str = "a"


def build_assembly(params: AssemblyParameters | None = None) -> cq.Assembly:
    """Create a CadQuery assembly with barrel, receiver, and stock."""
    params = params or AssemblyParameters()
    shell = params.shell

    assembly = cq.Assembly(name="havoc_water_gun_shell_rev_a")
    assembly.add(
        build_receiver(shell),
        name="receiver",
        color=cq.Color(0.75, 0.12, 0.12, 1.0),
    )
    assembly.add(
        build_barrel(shell),
        name="barrel",
        color=cq.Color(0.2, 0.2, 0.22, 1.0),
    )
    assembly.add(
        build_stock(shell),
        name="stock",
        color=cq.Color(0.15, 0.15, 0.18, 1.0),
    )
    return assembly


def build_compound(params: AssemblyParameters | None = None) -> cq.Workplane:
    """Return a fused Workplane of the full empty shell."""
    params = params or AssemblyParameters()
    return build_full_shell(params.shell)


if __name__ == "__main__":
    compound = build_compound()
    print(f"Assembly solid count: {len(compound.solids().vals())}")

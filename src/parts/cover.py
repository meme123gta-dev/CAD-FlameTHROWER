"""
Part name: Electronics enclosure lid / cover
Purpose: Removable lid for the low-voltage electronics enclosure.
Units: millimeters
Revision: A

This module wraps the lid builder from the enclosure parameter set so lid-only
workflows can import a dedicated cover part module.
"""

from __future__ import annotations

import cadquery as cq

from src.parts.enclosure import EnclosureParameters, build_lid, export_enclosure


def build_part(params: EnclosureParameters | None = None) -> cq.Workplane:
    """Build the enclosure lid/cover solid."""
    return build_lid(params)


def export_cover(params: EnclosureParameters | None = None) -> dict:
    """Export base and lid together using the enclosure exporter."""
    return export_enclosure(params)


if __name__ == "__main__":
    model = build_part()
    print(f"Lid solid count: {len(model.solids().vals())}")

"""
Part name: Amazon tank packing reference — ASIN B0BSDYNDQP
Purpose: Exact-size exterior solid of the SJVLXHI Ø3×10 in aluminum cylinder
         for fit checks / Tinkercad import in the theatrical water-gun shell.
Units: millimeters
Revision: A

Safety:
- Reference geometry for inert water/fluid packing only.
- Do not design fuel, ignition, combustion, or flame systems around this part.
- Listing is sold as a mini-bike fuel tank; this repo uses dimensions only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import cadquery as cq

from src.common.constants import INCH_TO_MM
from src.common.exporters import export_part_formats
from src.common.validation import validate_model

PRODUCT_NAME = "hardware_tank"
REVISION = "a"
VARIANT = "b0bsdyndqp"
ASIN = "B0BSDYNDQP"
AMAZON_URL = "https://www.amazon.com/dp/B0BSDYNDQP"


@dataclass(frozen=True)
class TankParameters:
    """Seller-listed dimensions for Amazon ASIN B0BSDYNDQP."""

    outer_diameter_mm: float = 3.0 * INCH_TO_MM  # 76.2
    length_mm: float = 10.0 * INCH_TO_MM  # 254.0
    capacity_gal_approx: float = 0.31

    # Center outlet (1/8 in) — radial boss + stub on cylinder wall.
    outlet_npt_in: float = 0.125
    outlet_boss_od_mm: float = 12.0
    outlet_boss_length_mm: float = 14.0
    outlet_stub_od_mm: float = 0.125 * INCH_TO_MM  # ~3.175
    outlet_stub_length_mm: float = 8.0
    outlet_offset_along_axis_mm: float = 0.0  # mid-length (ASSUMPTION T1)

    end_cap_od_mm: float = 3.0 * INCH_TO_MM + 2.0
    end_cap_length_mm: float = 8.0

    wall_thickness_mm: float = 1.5
    hollow: bool = True

    revision: str = REVISION


def validate_parameters(params: TankParameters) -> None:
    if params.outer_diameter_mm <= 0 or params.length_mm <= 0:
        raise ValueError("tank diameter and length must be positive")
    if params.hollow and params.wall_thickness_mm * 2 >= params.outer_diameter_mm:
        raise ValueError("wall_thickness_mm too large for hollow tank")
    if params.outlet_boss_od_mm <= params.outlet_stub_od_mm:
        raise ValueError("outlet boss must be larger than stub")


def _fuse(workplane: cq.Workplane) -> cq.Workplane:
    solids = workplane.solids().vals()
    if not solids:
        raise ValueError("no solids")
    if len(solids) == 1:
        return workplane
    fused = solids[0]
    for solid in solids[1:]:
        fused = fused.fuse(solid)
    return cq.Workplane("XY").newObject([fused])


def build_tank(params: TankParameters | None = None) -> cq.Workplane:
    """Build the cylindrical tank solid.

    Coordinate system:
    - Origin at geometric center of the cylinder.
    - +X along tank axis (length).
    - Center outlet boss points +Y.
    """
    params = params or TankParameters()
    validate_parameters(params)

    r = params.outer_diameter_mm / 2.0
    body = (
        cq.Workplane("YZ")
        .workplane(offset=-params.length_mm / 2.0)
        .circle(r)
        .extrude(params.length_mm)
    )

    if params.hollow:
        inner_r = r - params.wall_thickness_mm
        cavity = (
            cq.Workplane("YZ")
            .workplane(offset=-params.length_mm / 2.0 + params.wall_thickness_mm)
            .circle(inner_r)
            .extrude(params.length_mm - 2 * params.wall_thickness_mm)
        )
        body = body.cut(cavity)

    # Cosmetic end-cap rings flush with each end.
    left_cap = (
        cq.Workplane("YZ")
        .workplane(offset=-params.length_mm / 2.0)
        .circle(params.end_cap_od_mm / 2.0)
        .extrude(params.end_cap_length_mm)
    )
    right_cap = (
        cq.Workplane("YZ")
        .workplane(offset=params.length_mm / 2.0 - params.end_cap_length_mm)
        .circle(params.end_cap_od_mm / 2.0)
        .extrude(params.end_cap_length_mm)
    )
    body = body.union(left_cap).union(right_cap)

    # Center outlet boss + stub along +Y (seller: 1/8 in center outlet).
    outlet_x = params.outlet_offset_along_axis_mm
    boss = (
        cq.Workplane("XZ")
        .workplane(offset=r - 1.0)
        .center(outlet_x, 0.0)
        .circle(params.outlet_boss_od_mm / 2.0)
        .extrude(params.outlet_boss_length_mm)
    )
    stub = (
        cq.Workplane("XZ")
        .workplane(offset=r - 1.0 + params.outlet_boss_length_mm - 1.0)
        .center(outlet_x, 0.0)
        .circle(params.outlet_stub_od_mm / 2.0)
        .extrude(params.outlet_stub_length_mm)
    )
    bore = (
        cq.Workplane("XZ")
        .workplane(offset=r - 2.0)
        .center(outlet_x, 0.0)
        .circle(max(params.outlet_stub_od_mm / 2.0 - 0.4, 0.6))
        .extrude(params.outlet_boss_length_mm + params.outlet_stub_length_mm + 4.0)
    )
    return _fuse(body.union(boss).union(stub).cut(bore))


def parameters_dict(params: TankParameters) -> dict:
    data = asdict(params)
    data["asin"] = ASIN
    data["amazon_url"] = AMAZON_URL
    data["brand"] = "SJVLXHI"
    data["outer_diameter_in"] = 3.0
    data["length_in"] = 10.0
    data["capacity_L_approx"] = params.capacity_gal_approx * 3.785411784
    data["spec_path"] = "specifications/hardware_tank_B0BSDYNDQP.md"
    data["port_roles"] = {
        "center_outlet": {
            "direction": "+Y",
            "role": "tank fluid outlet (seller: 1/8 in center outlet)",
            "note": "Single center outlet on cylinder wall; no separate pickup listed",
        }
    }
    return data


def export_tank(
    params: TankParameters | None = None,
    *,
    stl_quality: str = "normal",
) -> dict[str, Path]:
    params = params or TankParameters()
    solid = build_tank(params)
    validate_model(solid, expected_solid_count=1, min_volume_mm3=100.0)
    return export_part_formats(
        solid,
        product=PRODUCT_NAME,
        part="cylinder",
        variant=VARIANT,
        revision=params.revision,
        stl_quality=stl_quality,
    )


if __name__ == "__main__":
    p = TankParameters()
    print(f"Tank {ASIN}: Ø{p.outer_diameter_mm:.1f} x {p.length_mm:.1f} mm")
    for fmt, path in export_tank(p).items():
        print(f"  {fmt}: {path}")

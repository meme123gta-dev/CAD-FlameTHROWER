"""
Part name: Amazon motor/pump packing reference — ASIN B07NYZ2CGK
Purpose: Exact-envelope solid of the FTVOGUE VN-C4 DC12V 42W oilless vacuum pump
         for fit checks / Tinkercad import in the theatrical water-gun shell.
Units: millimeters
Revision: A

Safety:
- Reference geometry for water-pump / vacuum packing only (theatrical water gun).
- Do not design fuel, ignition, combustion, pressurized flame, or weapon systems.
- Port roles below are from the seller installation diagram (AIR INLET / AIR OUTLET).

Coordinate system:
- Origin at bottom center of the mounting plate (Z=0 on plate bottom).
- +X toward motor end; -X toward pump-head free end.
- +Z up.
- PICKUP (AIR INLET): side port on pump head, facing toward the motor (+X).
- OUTPUT (AIR OUTLET): top port on pump head (+Z).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import cadquery as cq

from src.common.exporters import export_part_formats
from src.common.validation import validate_model

PRODUCT_NAME = "hardware_motor"
REVISION = "a"
VARIANT = "b07nyz2cgk"
ASIN = "B07NYZ2CGK"
AMAZON_URL = "https://www.amazon.com/dp/B07NYZ2CGK"
MODEL_NUMBER = "VN-C4"


@dataclass(frozen=True)
class MotorParameters:
    """Seller-listed envelope for Amazon ASIN B07NYZ2CGK (FTVOGUE VN-C4)."""

    # Overall envelope from seller dimension diagram.
    overall_length_mm: float = 90.0
    overall_width_mm: float = 44.0
    overall_height_mm: float = 110.0

    # Electrical / performance (listing).
    rated_voltage_v: float = 12.0
    working_voltage_min_v: float = 9.0
    working_voltage_max_v: float = 14.0
    power_w: float = 42.0
    flow_l_per_min: float = 40.0
    vacuum_kpa: float = -85.0
    mass_g: float = 488.0

    # Motor can (ASSUMPTION M1: ~775-class Ø42 mm from listing photos).
    motor_diameter_mm: float = 42.0
    motor_length_mm: float = 48.0

    # Black pump head block (ASSUMPTION M2: sized so plate + head + top outlet ≈ 110 mm).
    pump_length_mm: float = 40.0
    pump_width_mm: float = 44.0
    pump_height_mm: float = 92.0

    # Mounting plate under assembly.
    plate_thickness_mm: float = 2.5
    plate_length_mm: float = 90.0
    plate_width_mm: float = 52.0
    mount_hole_diameter_mm: float = 3.5
    mount_hole_spacing_x_mm: float = 70.0
    mount_hole_spacing_y_mm: float = 40.0

    # Hose barbs — seller "Interface Diameter: 8mm".
    port_od_mm: float = 8.0
    port_id_mm: float = 5.0
    port_length_mm: float = 14.0

    # Flange between motor and pump head.
    flange_thickness_mm: float = 6.0
    flange_od_mm: float = 48.0

    revision: str = REVISION


def validate_parameters(params: MotorParameters) -> None:
    positive = (
        params.overall_length_mm,
        params.overall_width_mm,
        params.overall_height_mm,
        params.motor_diameter_mm,
        params.motor_length_mm,
        params.pump_length_mm,
        params.pump_width_mm,
        params.pump_height_mm,
        params.port_od_mm,
    )
    if any(v <= 0 for v in positive):
        raise ValueError("all primary motor dimensions must be positive")
    if params.port_id_mm >= params.port_od_mm:
        raise ValueError("port inner diameter must be smaller than outer")
    if params.pump_length_mm + params.motor_length_mm > params.overall_length_mm + 5.0:
        raise ValueError("pump + motor length exceeds overall envelope")


def _fuse(workplane: cq.Workplane) -> cq.Workplane:
    solids = workplane.solids().vals()
    if not solids:
        raise ValueError("no solids")
    if len(solids) == 1:
        return workplane
    fused = solids[0]
    for solid in solids[1:]:
        fused = fused.fuse(solid)
    result = cq.Workplane("XY").newObject([fused])
    remaining = result.solids().vals()
    if len(remaining) == 1:
        return result
    fused2 = remaining[0]
    for solid in remaining[1:]:
        fused2 = fused2.fuse(solid)
    return cq.Workplane("XY").newObject([fused2])


def build_motor(params: MotorParameters | None = None) -> cq.Workplane:
    """Build the vacuum-pump reference solid with labeled port roles in docs.

    Port roles (from seller installation diagram):
    - PICKUP / AIR INLET: hose barb on pump head facing the motor (+X direction stub)
    - OUTPUT / AIR OUTLET: hose barb on top of pump head (+Z)
    """
    params = params or MotorParameters()
    validate_parameters(params)

    # Mounting plate at Z=0..plate_thickness.
    plate = (
        cq.Workplane("XY")
        .box(
            params.plate_length_mm,
            params.plate_width_mm,
            params.plate_thickness_mm,
            centered=(True, True, False),
        )
    )
    # Four mounting holes.
    hx = params.mount_hole_spacing_x_mm / 2.0
    hy = params.mount_hole_spacing_y_mm / 2.0
    for x, y in ((-hx, -hy), (-hx, hy), (hx, -hy), (hx, hy)):
        hole = (
            cq.Workplane("XY")
            .workplane(offset=-0.5)
            .center(x, y)
            .circle(params.mount_hole_diameter_mm / 2.0)
            .extrude(params.plate_thickness_mm + 1.0)
        )
        plate = plate.cut(hole)

    # Pump head centered toward -X.
    pump_cx = -params.overall_length_mm / 2.0 + params.pump_length_mm / 2.0
    pump = (
        cq.Workplane("XY")
        .workplane(offset=params.plate_thickness_mm)
        .center(pump_cx, 0.0)
        .box(
            params.pump_length_mm,
            params.pump_width_mm,
            params.pump_height_mm,
            centered=(True, True, False),
        )
    )

    # Cooling-style grooves on pump ±Y faces (cosmetic).
    for sign in (-1.0, 1.0):
        for i in range(4):
            gz = params.plate_thickness_mm + 12.0 + i * 12.0
            if gz > params.plate_thickness_mm + params.pump_height_mm - 8.0:
                break
            groove = (
                cq.Workplane("XY")
                .workplane(offset=gz)
                .center(pump_cx, sign * (params.pump_width_mm / 2.0 - 1.0))
                .box(params.pump_length_mm * 0.7, 3.0, 3.0)
            )
            pump = pump.cut(groove)

    # Flange between pump and motor.
    flange_cx = pump_cx + params.pump_length_mm / 2.0 + params.flange_thickness_mm / 2.0
    flange_cz = params.plate_thickness_mm + params.motor_diameter_mm / 2.0 + 4.0
    flange = (
        cq.Workplane("YZ")
        .workplane(offset=flange_cx - params.flange_thickness_mm / 2.0)
        .center(0.0, flange_cz)
        .circle(params.flange_od_mm / 2.0)
        .extrude(params.flange_thickness_mm)
    )

    # Motor can along +X.
    motor_cx = (
        flange_cx
        + params.flange_thickness_mm / 2.0
        + params.motor_length_mm / 2.0
    )
    motor_cz = flange_cz
    motor = (
        cq.Workplane("YZ")
        .workplane(offset=motor_cx - params.motor_length_mm / 2.0)
        .center(0.0, motor_cz)
        .circle(params.motor_diameter_mm / 2.0)
        .extrude(params.motor_length_mm)
    )

    # --- PORTS ---
    # PICKUP (AIR INLET): barb on pump head face toward motor (+X).
    inlet_x = pump_cx + params.pump_length_mm / 2.0 - 2.0
    inlet_z = params.plate_thickness_mm + params.pump_height_mm * 0.55
    inlet = (
        cq.Workplane("YZ")
        .workplane(offset=inlet_x)
        .center(0.0, inlet_z)
        .circle(params.port_od_mm / 2.0)
        .extrude(params.port_length_mm)
    )
    inlet_bore = (
        cq.Workplane("YZ")
        .workplane(offset=inlet_x - 1.0)
        .center(0.0, inlet_z)
        .circle(params.port_id_mm / 2.0)
        .extrude(params.port_length_mm + 4.0)
    )

    # OUTPUT (AIR OUTLET): barb on top of pump head (+Z).
    outlet_x = pump_cx - params.pump_length_mm * 0.15
    outlet_z = params.plate_thickness_mm + params.pump_height_mm - 1.0
    outlet = (
        cq.Workplane("XY")
        .workplane(offset=outlet_z)
        .center(outlet_x, 0.0)
        .circle(params.port_od_mm / 2.0)
        .extrude(params.port_length_mm)
    )
    outlet_bore = (
        cq.Workplane("XY")
        .workplane(offset=outlet_z - 2.0)
        .center(outlet_x, 0.0)
        .circle(params.port_id_mm / 2.0)
        .extrude(params.port_length_mm + 4.0)
    )

    # Terminal nubs on motor free end (cosmetic).
    terminal_x = motor_cx + params.motor_length_mm / 2.0
    terminals = cq.Workplane("XY")
    for dy in (-6.0, 6.0):
        terminals = terminals.union(
            cq.Workplane("YZ")
            .workplane(offset=terminal_x)
            .center(dy, motor_cz + 8.0)
            .box(4.0, 3.0, 6.0)
        )

    body = (
        plate.union(pump)
        .union(flange)
        .union(motor)
        .union(inlet)
        .union(outlet)
        .union(terminals)
        .cut(inlet_bore)
        .cut(outlet_bore)
    )
    return _fuse(body)


def parameters_dict(params: MotorParameters) -> dict:
    data = asdict(params)
    data["asin"] = ASIN
    data["amazon_url"] = AMAZON_URL
    data["brand"] = "FTVOGUE"
    data["model_number"] = MODEL_NUMBER
    data["spec_path"] = f"specifications/hardware_motor_{ASIN}.md"
    data["port_roles"] = {
        "pickup_air_inlet": {
            "direction": "+X (toward motor, on pump-head face)",
            "role": "PICKUP / AIR INLET (suction / vacuum)",
            "port_od_mm": params.port_od_mm,
            "evidence": "Seller installation diagram labels AIR INLET on pump head; "
            "vacuum created at inlet (-85 kPa)",
        },
        "output_air_outlet": {
            "direction": "+Z (top of pump head)",
            "role": "OUTPUT / AIR OUTLET (discharge / exhaust)",
            "port_od_mm": params.port_od_mm,
            "evidence": "Seller installation diagram labels AIR OUTLET on top; "
            "exhaust hose connects here",
        },
    }
    data["assumptions"] = [
        "M1: motor can OD ≈ 42 mm (775-class appearance in listing photos)",
        "M2: pump-head block sized to fit inside 90×44×110 mm envelope",
        "M3: mount-hole spacing assumed 70×40 mm (not seller-listed; verify on unit)",
        "M4: dual-chamber listings show 2+2 ports; this reference models the primary "
        "INLET and OUTLET barbs from the installation diagram (one each)",
    ]
    return data


def export_motor(
    params: MotorParameters | None = None,
    *,
    stl_quality: str = "normal",
) -> dict[str, Path]:
    params = params or MotorParameters()
    solid = build_motor(params)
    validate_model(solid, expected_solid_count=1, min_volume_mm3=100.0)
    return export_part_formats(
        solid,
        product=PRODUCT_NAME,
        part="vacuum_pump",
        variant=VARIANT,
        revision=params.revision,
        stl_quality=stl_quality,
    )


if __name__ == "__main__":
    p = MotorParameters()
    print(
        f"Motor {ASIN} {MODEL_NUMBER}: "
        f"{p.overall_length_mm:.0f}×{p.overall_width_mm:.0f}×{p.overall_height_mm:.0f} mm"
    )
    print("PICKUP = AIR INLET (toward motor); OUTPUT = AIR OUTLET (top)")
    for fmt, path in export_motor(p).items():
        print(f"  {fmt}: {path}")

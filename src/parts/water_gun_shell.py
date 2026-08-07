"""
Part name: Havoc-inspired theatrical water-gun empty shell
Purpose: Printable exterior enclosure for a display/theatrical water-gun prop.
Units: millimeters
Revision: B

Coordinate system:
- Origin at the geometric center of the receiver outer XY envelope.
- +X toward muzzle (barrel), -X toward stock, +Y right, +Z up.
- Z = 0 at the exterior bottom of the receiver.

Safety:
- Empty exterior shell and placeholder exclusion zones only.
- No fuel, ignition, combustion, pressurized-gas, flame, or weapon systems.
- Tank and pump/motor regions are inert cavities sized for water/fluid hardware packing.
- Barrel bore = water-nozzle packing path; barrel conduit = inert low-voltage wiring /
  sensor chase only (NOT high-voltage ignition or spark systems).
- Theatrical/display use; structural capacity not verified.
- Inspired by Apex Legends Havoc silhouette proportions only — not a licensed replica.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import cadquery as cq

from src.common.constants import DEFAULT_MIN_WALL_MM, INCH_TO_MM
from src.common.exporters import export_part_formats
from src.common.validation import validate_model

PRODUCT_NAME = "havoc_water_gun_shell"
REVISION = "b"
VARIANT = "default"


@dataclass(frozen=True)
class WaterGunShellParameters:
    """Parametric empty shell sized for a ~2.5 gal tank and dual pump footprints.

    Rev B adds tank cradle ribs, stock motor bay, barrel water+conduit dual channel,
    side panel ribs, and a hose tunnel toward the barrel (packing envelopes only).
    """

    # Receiver (mid-body / tank bay) — thick central section.
    receiver_length_mm: float = 380.0
    receiver_width_mm: float = 280.0
    receiver_height_mm: float = 280.0

    # Long barrel shroud (water-nozzle bore + inert conduit chase).
    barrel_length_mm: float = 420.0
    barrel_outer_diameter_front_mm: float = 72.0
    barrel_outer_diameter_rear_mm: float = 92.0
    barrel_bore_diameter_mm: float = 40.0
    # Inert LV wiring/sensor chase above the water bore (NOT HV ignition).
    barrel_conduit_diameter_mm: float = 18.0
    barrel_conduit_offset_z_mm: float = 32.0
    barrel_shroud_width_mm: float = 110.0
    barrel_shroud_height_mm: float = 110.0
    barrel_side_rib_count: int = 8
    barrel_side_rib_depth_mm: float = 4.0
    barrel_side_rib_width_mm: float = 8.0

    # Thick stubby stock for pump-motor + batteries / low-voltage components.
    stock_length_mm: float = 200.0
    stock_width_mm: float = 150.0
    stock_height_mm: float = 170.0

    wall_thickness_mm: float = 3.2
    corner_radius_mm: float = 8.0

    # ~2.5 gal go-kart style tank exclusion zone (ASSUMPTION A1).
    # Spun tanks are often ~12 x 8 in; rectangular plastics are similar.
    tank_cavity_length_mm: float = 330.0
    tank_cavity_width_mm: float = 220.0
    tank_cavity_height_mm: float = 220.0
    tank_clearance_mm: float = 10.0
    tank_access_open_top: bool = True
    # Cylindrical cradle diameter for spun-style tanks (ASSUMPTION A7).
    tank_cradle_diameter_mm: float = 210.0
    tank_cradle_rib_count: int = 4
    tank_cradle_rib_width_mm: float = 12.0

    # Horizontal water pump exclusion (ASSUMPTION A2).
    h_pump_length_mm: float = 160.0
    h_pump_width_mm: float = 100.0
    h_pump_height_mm: float = 100.0

    # Vertical water pump exclusion (ASSUMPTION A3).
    v_pump_diameter_mm: float = 100.0
    v_pump_height_mm: float = 180.0

    # Battery / component bay inside stock (ASSUMPTION A4).
    battery_cavity_length_mm: float = 70.0
    battery_cavity_width_mm: float = 100.0
    battery_cavity_height_mm: float = 90.0

    # Pump-motor bay in stock (ASSUMPTION A8) — water-pump motor packing only.
    motor_cavity_length_mm: float = 95.0
    motor_cavity_diameter_mm: float = 72.0
    motor_mount_boss_diameter_mm: float = 16.0
    motor_mount_boss_height_mm: float = 8.0

    # Hose tunnel from receiver pump bay into barrel (packing only).
    hose_tunnel_diameter_mm: float = 28.0

    # Cosmetic empty pistol-grip stub under the receiver (not load-rated).
    grip_length_mm: float = 125.0
    grip_width_mm: float = 44.0
    grip_height_mm: float = 120.0
    grip_offset_x_mm: float = -35.0
    grip_rake_deg: float = 12.0

    # Top rail / carry-handle ridge (cosmetic).
    rail_length_mm: float = 260.0
    rail_width_mm: float = 28.0
    rail_height_mm: float = 18.0

    # Receiver side cooling-style panel ribs (cosmetic, Havoc-inspired).
    receiver_side_rib_count: int = 6
    receiver_side_rib_depth_mm: float = 6.0
    receiver_side_rib_width_mm: float = 10.0

    # Mating lip between length modules (stub flanges).
    flange_depth_mm: float = 12.0
    flange_clearance_mm: float = 0.40

    # Split-plane kerf for left/right printable halves.
    split_kerf_mm: float = 0.20

    # Target printer envelope (Bambu Lab P1S default).
    printer_bed_x_mm: float = 256.0
    printer_bed_y_mm: float = 256.0
    printer_bed_z_mm: float = 256.0

    revision: str = REVISION


def validate_parameters(params: WaterGunShellParameters) -> None:
    """Raise ValueError when parameters cannot form a valid empty shell."""
    positive_fields = (
        params.receiver_length_mm,
        params.receiver_width_mm,
        params.receiver_height_mm,
        params.barrel_length_mm,
        params.barrel_outer_diameter_front_mm,
        params.barrel_outer_diameter_rear_mm,
        params.barrel_bore_diameter_mm,
        params.barrel_conduit_diameter_mm,
        params.stock_length_mm,
        params.stock_width_mm,
        params.stock_height_mm,
        params.wall_thickness_mm,
        params.tank_cavity_length_mm,
        params.tank_cavity_width_mm,
        params.tank_cavity_height_mm,
        params.tank_cradle_diameter_mm,
        params.h_pump_length_mm,
        params.h_pump_width_mm,
        params.h_pump_height_mm,
        params.v_pump_diameter_mm,
        params.v_pump_height_mm,
        params.battery_cavity_length_mm,
        params.battery_cavity_width_mm,
        params.battery_cavity_height_mm,
        params.motor_cavity_length_mm,
        params.motor_cavity_diameter_mm,
        params.hose_tunnel_diameter_mm,
    )
    if any(value <= 0 for value in positive_fields):
        raise ValueError("all primary dimensions must be positive")

    if params.wall_thickness_mm < DEFAULT_MIN_WALL_MM:
        raise ValueError(
            f"wall_thickness_mm must be >= {DEFAULT_MIN_WALL_MM} for FDM durability"
        )

    if params.barrel_bore_diameter_mm >= min(
        params.barrel_outer_diameter_front_mm,
        params.barrel_outer_diameter_rear_mm,
    ):
        raise ValueError("barrel bore must be smaller than outer barrel diameters")

    bore_r = params.barrel_bore_diameter_mm / 2.0
    conduit_r = params.barrel_conduit_diameter_mm / 2.0
    inner_half_h = params.barrel_shroud_height_mm / 2.0 - params.wall_thickness_mm
    if bore_r >= inner_half_h:
        raise ValueError("barrel bore does not fit shroud height with walls")
    if abs(params.barrel_conduit_offset_z_mm) + conduit_r >= inner_half_h:
        raise ValueError("barrel conduit does not fit shroud height with walls")
    if abs(params.barrel_conduit_offset_z_mm) < bore_r + conduit_r + 2.0:
        raise ValueError("barrel bore and conduit overlap inside the shroud")

    tank_l = params.tank_cavity_length_mm + 2 * params.tank_clearance_mm
    tank_w = params.tank_cavity_width_mm + 2 * params.tank_clearance_mm
    tank_h = params.tank_cavity_height_mm + params.tank_clearance_mm
    if tank_l + 2 * params.wall_thickness_mm > params.receiver_length_mm:
        raise ValueError("tank cavity does not fit receiver length with walls")
    if tank_w + 2 * params.wall_thickness_mm > params.receiver_width_mm:
        raise ValueError("tank cavity does not fit receiver width with walls")
    if tank_h + 2 * params.wall_thickness_mm > params.receiver_height_mm:
        raise ValueError("tank cavity does not fit receiver height with walls")

    if params.tank_cradle_diameter_mm + 2 * params.wall_thickness_mm > params.receiver_width_mm:
        raise ValueError("tank cradle diameter does not fit receiver width")

    if (
        params.battery_cavity_length_mm + params.motor_cavity_length_mm
        + 3 * params.wall_thickness_mm
        > params.stock_length_mm
    ):
        raise ValueError("battery + motor cavities do not fit stock length")
    if (
        max(params.battery_cavity_width_mm, params.motor_cavity_diameter_mm)
        + 2 * params.wall_thickness_mm
        > params.stock_width_mm
    ):
        raise ValueError("battery/motor cavities do not fit stock width")
    if (
        max(params.battery_cavity_height_mm, params.motor_cavity_diameter_mm)
        + params.wall_thickness_mm
        > params.stock_height_mm
    ):
        raise ValueError("battery/motor cavities do not fit stock height")

    if params.corner_radius_mm < 0:
        raise ValueError("corner_radius_mm must be non-negative")

    if params.split_kerf_mm < 0:
        raise ValueError("split_kerf_mm must be non-negative")

    if params.receiver_side_rib_count < 0 or params.barrel_side_rib_count < 0:
        raise ValueError("rib counts must be non-negative")


def overall_length_mm(params: WaterGunShellParameters) -> float:
    return (
        params.stock_length_mm
        + params.receiver_length_mm
        + params.barrel_length_mm
    )


def overall_width_mm(params: WaterGunShellParameters) -> float:
    return max(
        params.receiver_width_mm,
        params.stock_width_mm,
        params.barrel_shroud_width_mm,
        params.barrel_outer_diameter_rear_mm,
    )


def overall_height_mm(params: WaterGunShellParameters) -> float:
    # Grip hangs below receiver bottom; rail sits on top.
    return (
        params.receiver_height_mm
        + params.grip_height_mm
        + params.rail_height_mm
    )


def _receiver_x_span(params: WaterGunShellParameters) -> tuple[float, float]:
    half = params.receiver_length_mm / 2.0
    return (-half, half)


def _barrel_x_span(params: WaterGunShellParameters) -> tuple[float, float]:
    _, receiver_max = _receiver_x_span(params)
    return (receiver_max, receiver_max + params.barrel_length_mm)


def _stock_x_span(params: WaterGunShellParameters) -> tuple[float, float]:
    receiver_min, _ = _receiver_x_span(params)
    return (receiver_min - params.stock_length_mm, receiver_min)


def _fuse_solids(workplane: cq.Workplane) -> cq.Workplane:
    solids = workplane.solids().vals()
    if not solids:
        raise ValueError("boolean result contains no solids")
    if len(solids) == 1:
        return workplane
    fused = solids[0]
    for solid in solids[1:]:
        fused = fused.fuse(solid)
    # fuse() can return a compound; flatten to a single solid when possible.
    result = cq.Workplane("XY").newObject([fused])
    remaining = result.solids().vals()
    if len(remaining) == 1:
        return result
    fused2 = remaining[0]
    for solid in remaining[1:]:
        fused2 = fused2.fuse(solid)
    result2 = cq.Workplane("XY").newObject([fused2])
    if len(result2.solids().vals()) != 1:
        volumes = [round(s.Volume(), 1) for s in result2.solids().vals()]
        raise ValueError(
            f"unable to fuse into a single solid; volumes_mm3={volumes}"
        )
    return result2


def _rounded_box_at(
    *,
    length_mm: float,
    width_mm: float,
    height_mm: float,
    center_xyz: tuple[float, float, float],
    corner_radius_mm: float = 0.0,
) -> cq.Workplane:
    cx, cy, cz = center_xyz
    box = (
        cq.Workplane("XY")
        .workplane(offset=cz)
        .center(cx, cy)
        .box(length_mm, width_mm, height_mm)
    )
    if corner_radius_mm > 0:
        max_r = min(length_mm, width_mm) / 2.0 - 0.1
        radius = min(corner_radius_mm, max_r)
        if radius > 0.2:
            try:
                box = box.edges("|Z").fillet(radius)
            except Exception:
                pass
    return box


def build_receiver(params: WaterGunShellParameters | None = None) -> cq.Workplane:
    """Build the hollow mid-body with tank cradle, pump bays, and side ribs."""
    params = params or WaterGunShellParameters()
    validate_parameters(params)

    wall = params.wall_thickness_mm
    rx0, rx1 = _receiver_x_span(params)
    rx_center = (rx0 + rx1) / 2.0

    outer = _rounded_box_at(
        length_mm=params.receiver_length_mm,
        width_mm=params.receiver_width_mm,
        height_mm=params.receiver_height_mm,
        center_xyz=(rx_center, 0.0, params.receiver_height_mm / 2.0),
        corner_radius_mm=params.corner_radius_mm,
    )

    # Interior cavity leaves both floor and roof thickness.
    inner_length = params.receiver_length_mm - 2 * wall
    inner_width = params.receiver_width_mm - 2 * wall
    inner_height = params.receiver_height_mm - 2 * wall
    cavity = _rounded_box_at(
        length_mm=inner_length,
        width_mm=inner_width,
        height_mm=inner_height,
        center_xyz=(
            rx_center,
            0.0,
            wall + inner_height / 2.0,
        ),
        corner_radius_mm=max(params.corner_radius_mm - wall, 0.0),
    )
    body = outer.cut(cavity)

    if params.tank_access_open_top:
        # Hatch through the roof for tank drop-in; keep forward roof for the rail.
        hatch_length = min(200.0, inner_length - 140.0)
        hatch_width = min(
            params.tank_cavity_width_mm * 0.80,
            inner_width - 50.0,
        )
        hatch = _rounded_box_at(
            length_mm=hatch_length,
            width_mm=hatch_width,
            height_mm=wall + 4.0,
            center_xyz=(rx_center - 50.0, 0.0, params.receiver_height_mm),
        )
        body = body.cut(hatch)

    # Rectangular tank packing envelope.
    tank_l = params.tank_cavity_length_mm + 2 * params.tank_clearance_mm
    tank_w = params.tank_cavity_width_mm + 2 * params.tank_clearance_mm
    tank_h = params.tank_cavity_height_mm + params.tank_clearance_mm
    tank = _rounded_box_at(
        length_mm=min(tank_l, inner_length - 1.0),
        width_mm=min(tank_w, inner_width - 1.0),
        height_mm=min(tank_h, inner_height),
        center_xyz=(rx_center, 0.0, wall + min(tank_h, inner_height) / 2.0),
    )
    body = body.cut(tank)

    # Cylindrical cradle cut for spun-style tanks (better seating than box alone).
    cradle_len = min(params.tank_cavity_length_mm * 0.92, inner_length - 20.0)
    cradle_r = params.tank_cradle_diameter_mm / 2.0
    cradle_z = wall + cradle_r + 8.0
    cradle = (
        cq.Workplane("YZ")
        .workplane(offset=rx_center - cradle_len / 2.0)
        .center(0.0, cradle_z)
        .circle(cradle_r)
        .extrude(cradle_len)
    )
    body = body.cut(cradle)

    # Horizontal pump bay — forward lower area toward the barrel.
    h_cx = rx1 - wall - params.h_pump_length_mm / 2.0 - 8.0
    h_cz = wall + params.h_pump_height_mm / 2.0 + 4.0
    h_pump = _rounded_box_at(
        length_mm=params.h_pump_length_mm,
        width_mm=params.h_pump_width_mm,
        height_mm=params.h_pump_height_mm,
        center_xyz=(h_cx, 0.0, h_cz),
    )
    body = body.cut(h_pump)

    # Side access cut for horizontal pump packing (right side).
    h_access = _rounded_box_at(
        length_mm=params.h_pump_length_mm * 0.85,
        width_mm=params.receiver_width_mm / 2.0 + 2.0,
        height_mm=params.h_pump_height_mm * 0.85,
        center_xyz=(
            h_cx,
            params.receiver_width_mm / 4.0,
            h_cz,
        ),
    )
    body = body.cut(h_access)

    # Vertical pump bay — rear-left of tank volume.
    v_cx = rx0 + wall + params.v_pump_diameter_mm / 2.0 + 20.0
    v_cy = -params.receiver_width_mm / 2.0 + wall + params.v_pump_diameter_mm / 2.0 + 12.0
    v_cz = wall + params.v_pump_height_mm / 2.0
    v_pump = (
        cq.Workplane("XY")
        .workplane(offset=wall)
        .center(v_cx, v_cy)
        .circle(params.v_pump_diameter_mm / 2.0)
        .extrude(params.v_pump_height_mm + 1.0)
    )
    body = body.cut(v_pump)

    # Left-side access for vertical pump.
    v_access = _rounded_box_at(
        length_mm=params.v_pump_diameter_mm * 0.9,
        width_mm=params.receiver_width_mm / 2.0 + 2.0,
        height_mm=params.v_pump_height_mm * 0.9,
        center_xyz=(v_cx, -params.receiver_width_mm / 4.0, v_cz),
    )
    body = body.cut(v_access)

    # Hose tunnel from pump bay toward barrel (+X) — water packing path only.
    hose_z = h_cz
    hose = (
        cq.Workplane("YZ")
        .workplane(offset=h_cx)
        .center(0.0, hose_z)
        .circle(params.hose_tunnel_diameter_mm / 2.0)
        .extrude(rx1 - h_cx + 8.0)
    )
    body = body.cut(hose)

    # Cosmetic top rail / carry ridge on the forward roof (overlap for fusion).
    rail_overlap_mm = 3.0
    rail_length = min(params.rail_length_mm, 120.0)
    rail = _rounded_box_at(
        length_mm=rail_length,
        width_mm=params.rail_width_mm,
        height_mm=params.rail_height_mm + rail_overlap_mm,
        center_xyz=(
            rx1 - rail_length / 2.0 - 10.0,
            0.0,
            params.receiver_height_mm
            + params.rail_height_mm / 2.0
            - rail_overlap_mm / 2.0,
        ),
        corner_radius_mm=2.0,
    )
    body = body.union(rail)

    # Empty cosmetic grip stub under receiver (slight rake via offset).
    grip = _rounded_box_at(
        length_mm=params.grip_length_mm,
        width_mm=params.grip_width_mm,
        height_mm=params.grip_height_mm,
        center_xyz=(
            params.grip_offset_x_mm,
            0.0,
            -params.grip_height_mm / 2.0 + wall,
        ),
        corner_radius_mm=6.0,
    )
    grip_cavity = _rounded_box_at(
        length_mm=params.grip_length_mm - 2 * wall,
        width_mm=max(params.grip_width_mm - 2 * wall, 8.0),
        height_mm=params.grip_height_mm - wall,
        center_xyz=(
            params.grip_offset_x_mm,
            0.0,
            -params.grip_height_mm / 2.0 + wall / 2.0,
        ),
    )
    body = body.union(grip).cut(grip_cavity)

    # Finger scoop on forward face of grip (cosmetic recess — shallow, non-severing).
    scoop = _rounded_box_at(
        length_mm=16.0,
        width_mm=params.grip_width_mm + 4.0,
        height_mm=28.0,
        center_xyz=(
            params.grip_offset_x_mm + params.grip_length_mm / 2.0 - 6.0,
            0.0,
            -params.grip_height_mm * 0.40,
        ),
    )
    body = body.cut(scoop)

    # Angular Havoc-ish cheek plate on the right side (cosmetic solid boss).
    cheek = _rounded_box_at(
        length_mm=params.receiver_length_mm * 0.55,
        width_mm=18.0,
        height_mm=params.receiver_height_mm * 0.45,
        center_xyz=(
            rx_center + 20.0,
            params.receiver_width_mm / 2.0 + 6.0,
            params.receiver_height_mm * 0.55,
        ),
        corner_radius_mm=3.0,
    )
    body = body.union(cheek)

    # Side panel grooves (both sides) — recessed Havoc-style detailing.
    if params.receiver_side_rib_count > 0:
        rib_span = params.receiver_length_mm * 0.70
        rib_start = rx_center - rib_span / 2.0
        step = rib_span / max(params.receiver_side_rib_count - 1, 1)
        rib_h = params.receiver_height_mm * 0.50
        rib_z = params.receiver_height_mm * 0.45
        for i in range(params.receiver_side_rib_count):
            rib_x = rib_start + i * step
            for sign in (-1.0, 1.0):
                groove = _rounded_box_at(
                    length_mm=params.receiver_side_rib_width_mm,
                    width_mm=params.receiver_side_rib_depth_mm + 2.0,
                    height_mm=rib_h,
                    center_xyz=(
                        rib_x,
                        sign
                        * (
                            params.receiver_width_mm / 2.0
                            - params.receiver_side_rib_depth_mm / 2.0
                            + 0.5
                        ),
                        rib_z,
                    ),
                )
                body = body.cut(groove)

    return _fuse_solids(body)


def build_barrel(params: WaterGunShellParameters | None = None) -> cq.Workplane:
    """Build hollow barrel shroud: water bore + inert LV conduit + side ribs."""
    params = params or WaterGunShellParameters()
    validate_parameters(params)

    wall = params.wall_thickness_mm
    bx0, bx1 = _barrel_x_span(params)
    length = params.barrel_length_mm
    axis_z = params.receiver_height_mm * 0.55
    mid_x = (bx0 + bx1) / 2.0

    # Blocky Havoc-like shroud body.
    shroud = _rounded_box_at(
        length_mm=length,
        width_mm=params.barrel_shroud_width_mm,
        height_mm=params.barrel_shroud_height_mm,
        center_xyz=(mid_x, 0.0, axis_z),
        corner_radius_mm=4.0,
    )

    # External rear collar (larger than shroud so it fuses as an accent).
    rear_collar_od = max(
        params.barrel_outer_diameter_rear_mm,
        params.barrel_shroud_height_mm + 12.0,
    )
    rear_collar = (
        cq.Workplane("YZ")
        .workplane(offset=bx0)
        .center(0.0, axis_z)
        .circle(rear_collar_od / 2.0)
        .extrude(36.0)
    )

    # External front / muzzle collar (stepped).
    front_collar_od = max(
        params.barrel_outer_diameter_front_mm + 10.0,
        params.barrel_shroud_height_mm - 4.0,
    )
    front_collar = (
        cq.Workplane("YZ")
        .workplane(offset=bx1 - 40.0)
        .center(0.0, axis_z)
        .circle(front_collar_od / 2.0)
        .extrude(28.0)
    )
    muzzle_ring = (
        cq.Workplane("YZ")
        .workplane(offset=bx1 - 16.0)
        .center(0.0, axis_z)
        .circle(front_collar_od / 2.0 + 6.0)
        .extrude(16.0)
    )

    # Underslung rail overlapping the shroud bottom wall.
    under_rail = _rounded_box_at(
        length_mm=length * 0.7,
        width_mm=36.0,
        height_mm=28.0,
        center_xyz=(
            mid_x + length * 0.05,
            0.0,
            axis_z - params.barrel_shroud_height_mm / 2.0 - 4.0,
        ),
        corner_radius_mm=2.0,
    )

    # Top rib overlapping the shroud top wall.
    top_rib = _rounded_box_at(
        length_mm=length * 0.8,
        width_mm=22.0,
        height_mm=16.0,
        center_xyz=(
            mid_x,
            0.0,
            axis_z + params.barrel_shroud_height_mm / 2.0 + 2.0,
        ),
        corner_radius_mm=2.0,
    )

    body = (
        shroud.union(rear_collar)
        .union(front_collar)
        .union(muzzle_ring)
        .union(under_rail)
        .union(top_rib)
    )

    # Side panel grooves (recessed rail language from V3).
    if params.barrel_side_rib_count > 0:
        rib_span = length * 0.75
        rib_start = mid_x - rib_span / 2.0
        step = rib_span / max(params.barrel_side_rib_count - 1, 1)
        for i in range(params.barrel_side_rib_count):
            rib_x = rib_start + i * step
            for sign in (-1.0, 1.0):
                groove = _rounded_box_at(
                    length_mm=params.barrel_side_rib_width_mm,
                    width_mm=params.barrel_side_rib_depth_mm + 2.0,
                    height_mm=params.barrel_shroud_height_mm * 0.65,
                    center_xyz=(
                        rib_x,
                        sign
                        * (
                            params.barrel_shroud_width_mm / 2.0
                            - params.barrel_side_rib_depth_mm / 2.0
                            + 0.5
                        ),
                        axis_z,
                    ),
                )
                body = body.cut(groove)

    # Hollow the shroud interior (open toward +X and -X via overcut).
    inner = _rounded_box_at(
        length_mm=length + 2.0,
        width_mm=params.barrel_shroud_width_mm - 2 * wall,
        height_mm=params.barrel_shroud_height_mm - 2 * wall,
        center_xyz=(mid_x, 0.0, axis_z),
    )
    body = body.cut(inner)

    # Water-nozzle packing bore through collars / muzzle.
    bore = (
        cq.Workplane("YZ")
        .workplane(offset=bx0 - 1.0)
        .center(0.0, axis_z)
        .circle(params.barrel_bore_diameter_mm / 2.0)
        .extrude(length + 2.0)
    )
    body = body.cut(bore)

    # Inert LV wiring / sensor conduit above water bore (NOT HV ignition).
    conduit = (
        cq.Workplane("YZ")
        .workplane(offset=bx0 - 1.0)
        .center(0.0, axis_z + params.barrel_conduit_offset_z_mm)
        .circle(params.barrel_conduit_diameter_mm / 2.0)
        .extrude(length + 2.0)
    )
    body = body.cut(conduit)

    # Hose docking pocket at barrel rear (mates with receiver hose tunnel).
    hose_dock = (
        cq.Workplane("YZ")
        .workplane(offset=bx0 - 2.0)
        .center(0.0, axis_z - 10.0)
        .circle(params.hose_tunnel_diameter_mm / 2.0 + 2.0)
        .extrude(30.0)
    )
    body = body.cut(hose_dock)

    return _fuse_solids(body)


def build_stock(params: WaterGunShellParameters | None = None) -> cq.Workplane:
    """Build stubby stock with motor bay, battery bay, and mount bosses."""
    params = params or WaterGunShellParameters()
    validate_parameters(params)

    wall = params.wall_thickness_mm
    sx0, sx1 = _stock_x_span(params)
    sx_center = (sx0 + sx1) / 2.0
    # Stock sits slightly above receiver bottom for a stubby butt look.
    stock_bottom = 20.0
    stock_cz = stock_bottom + params.stock_height_mm / 2.0

    outer = _rounded_box_at(
        length_mm=params.stock_length_mm,
        width_mm=params.stock_width_mm,
        height_mm=params.stock_height_mm,
        center_xyz=(sx_center, 0.0, stock_cz),
        corner_radius_mm=params.corner_radius_mm,
    )

    # Forward motor bay (toward receiver) — water-pump motor packing only.
    motor_cx = sx1 - wall - params.motor_cavity_length_mm / 2.0 - 6.0
    motor_cz = stock_bottom + wall + params.motor_cavity_diameter_mm / 2.0 + 10.0
    motor = (
        cq.Workplane("YZ")
        .workplane(offset=motor_cx - params.motor_cavity_length_mm / 2.0)
        .center(0.0, motor_cz)
        .circle(params.motor_cavity_diameter_mm / 2.0)
        .extrude(params.motor_cavity_length_mm + 2.0)
    )
    body = outer.cut(motor)

    # Side access for motor packing.
    motor_access = _rounded_box_at(
        length_mm=params.motor_cavity_length_mm * 0.85,
        width_mm=params.stock_width_mm / 2.0 + 2.0,
        height_mm=params.motor_cavity_diameter_mm * 0.85,
        center_xyz=(motor_cx, params.stock_width_mm / 4.0, motor_cz),
    )
    body = body.cut(motor_access)

    # Rear battery / LV component bay.
    batt_cx = sx0 + wall + params.battery_cavity_length_mm / 2.0 + 8.0
    cavity = _rounded_box_at(
        length_mm=params.battery_cavity_length_mm + 2.0,
        width_mm=params.battery_cavity_width_mm,
        height_mm=params.battery_cavity_height_mm,
        center_xyz=(
            batt_cx,
            0.0,
            stock_bottom + wall + params.battery_cavity_height_mm / 2.0,
        ),
    )
    body = body.cut(cavity)

    # Butt-plate opening on -X face for component loading.
    butt_open = _rounded_box_at(
        length_mm=wall + 4.0,
        width_mm=params.battery_cavity_width_mm * 0.95,
        height_mm=params.battery_cavity_height_mm * 0.95,
        center_xyz=(
            sx0,
            0.0,
            stock_bottom + wall + params.battery_cavity_height_mm / 2.0,
        ),
    )
    body = body.cut(butt_open)

    # Top hatch opening for battery access.
    top_hatch = _rounded_box_at(
        length_mm=params.battery_cavity_length_mm * 0.7,
        width_mm=params.battery_cavity_width_mm * 0.7,
        height_mm=wall + 6.0,
        center_xyz=(
            batt_cx,
            0.0,
            stock_bottom + params.stock_height_mm,
        ),
    )
    body = body.cut(top_hatch)

    # Shoulder pad / butt swell (cosmetic).
    pad = _rounded_box_at(
        length_mm=24.0,
        width_mm=params.stock_width_mm + 16.0,
        height_mm=params.stock_height_mm * 0.85,
        center_xyz=(sx0 + 8.0, 0.0, stock_cz),
        corner_radius_mm=6.0,
    )
    body = body.union(pad)

    return _fuse_solids(body)


def build_full_shell(params: WaterGunShellParameters | None = None) -> cq.Workplane:
    """Union barrel + receiver + stock into one empty shell reference solid."""
    params = params or WaterGunShellParameters()
    validate_parameters(params)

    receiver = build_receiver(params)
    barrel = build_barrel(params)
    stock = build_stock(params)
    return _fuse_solids(receiver.union(barrel).union(stock))


def _split_half(
    model: cq.Workplane,
    *,
    keep_positive_y: bool,
    kerf_mm: float,
) -> cq.Workplane:
    """Keep the +Y or -Y half by cutting with an oversized half-space box."""
    bbox = model.val().BoundingBox()
    # Slightly oversized cutter to avoid coincident-face failures.
    pad = 5.0
    length = bbox.xlen + 2 * pad
    height = bbox.zlen + 2 * pad
    width = bbox.ylen + 2 * pad
    cx = (bbox.xmin + bbox.xmax) / 2.0
    cz = (bbox.zmin + bbox.zmax) / 2.0

    if keep_positive_y:
        # Remove everything with Y < kerf/2
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=cz)
            .center(cx, -width / 2.0 + kerf_mm / 2.0)
            .box(length, width, height)
        )
    else:
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=cz)
            .center(cx, width / 2.0 - kerf_mm / 2.0)
            .box(length, width, height)
        )
    return _fuse_solids(model.cut(cutter))


def _split_along_x(
    model: cq.Workplane,
    *,
    cut_x_mm: float,
    keep_positive_x: bool,
    kerf_mm: float,
) -> cq.Workplane:
    """Keep the +X or -X side of a cut plane at cut_x_mm."""
    bbox = model.val().BoundingBox()
    pad = 5.0
    length = bbox.xlen + 2 * pad
    width = bbox.ylen + 2 * pad
    height = bbox.zlen + 2 * pad
    cy = (bbox.ymin + bbox.ymax) / 2.0
    cz = (bbox.zmin + bbox.zmax) / 2.0

    if keep_positive_x:
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=cz)
            .center(cut_x_mm - length / 2.0 + kerf_mm / 2.0, cy)
            .box(length, width, height)
        )
    else:
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=cz)
            .center(cut_x_mm + length / 2.0 - kerf_mm / 2.0, cy)
            .box(length, width, height)
        )
    return _fuse_solids(model.cut(cutter))


def _fits_printer(
    model: cq.Workplane,
    params: WaterGunShellParameters,
) -> bool:
    bbox = model.val().BoundingBox()
    dims = sorted([bbox.xlen, bbox.ylen, bbox.zlen])
    bed = sorted(
        [params.printer_bed_x_mm, params.printer_bed_y_mm, params.printer_bed_z_mm]
    )
    return all(d <= b + 1e-6 for d, b in zip(dims, bed, strict=True))


def build_printable_halves(
    part: str,
    params: WaterGunShellParameters | None = None,
) -> dict[str, cq.Workplane]:
    """Return left/right printable halves for barrel, receiver, or stock."""
    params = params or WaterGunShellParameters()
    builders = {
        "barrel": build_barrel,
        "receiver": build_receiver,
        "stock": build_stock,
    }
    if part not in builders:
        raise KeyError(f"Unknown part '{part}'. Expected one of {sorted(builders)}")

    solid = builders[part](params)
    return {
        "left": _split_half(
            solid, keep_positive_y=False, kerf_mm=params.split_kerf_mm
        ),
        "right": _split_half(
            solid, keep_positive_y=True, kerf_mm=params.split_kerf_mm
        ),
    }


def p1s_parameters() -> WaterGunShellParameters:
    """Shell params tuned so length/side splits fit a Bambu Lab P1S (256^3).

    Grip is still modeled on the receiver for assembly reference, but P1S
    receiver print segments use a body-only cut that excludes the hanging grip
    envelope by relying on reduced receiver height + separate grip export.
    """
    return WaterGunShellParameters(
        # Keep tank packing, but cap outer height under the P1S Z limit when
        # grip is printed separately and rail stays short on the forward roof.
        receiver_length_mm=380.0,
        receiver_width_mm=280.0,
        receiver_height_mm=248.0,
        tank_cavity_length_mm=330.0,
        tank_cavity_width_mm=220.0,
        tank_cavity_height_mm=210.0,
        tank_clearance_mm=8.0,
        barrel_length_mm=420.0,
        stock_length_mm=200.0,
        stock_width_mm=150.0,
        stock_height_mm=170.0,
        grip_height_mm=110.0,
        rail_height_mm=12.0,
        printer_bed_x_mm=256.0,
        printer_bed_y_mm=256.0,
        printer_bed_z_mm=256.0,
        revision=REVISION,
    )


def build_p1s_segments(
    params: WaterGunShellParameters | None = None,
) -> dict[str, cq.Workplane]:
    """Build printable segments sized for Bambu Lab P1S beds.

    Layout:
    - stock_left / stock_right
    - barrel_{rear|front}_{left|right}
    - receiver_{rear|front}_{left|right}  (body; grip hanging volume trimmed)
    - grip (single cosmetic stub for optional separate print)
    """
    params = params or p1s_parameters()
    validate_parameters(params)
    kerf = params.split_kerf_mm
    segments: dict[str, cq.Workplane] = {}

    # Stock — already P1S-friendly as L/R halves.
    for side, solid in build_printable_halves("stock", params).items():
        segments[f"stock_{side}"] = solid

    # Barrel — split mid-length, then L/R.
    barrel = build_barrel(params)
    bx0, bx1 = _barrel_x_span(params)
    barrel_mid = (bx0 + bx1) / 2.0
    barrel_rear = _split_along_x(
        barrel, cut_x_mm=barrel_mid, keep_positive_x=False, kerf_mm=kerf
    )
    barrel_front = _split_along_x(
        barrel, cut_x_mm=barrel_mid, keep_positive_x=True, kerf_mm=kerf
    )
    for region_name, region in (("rear", barrel_rear), ("front", barrel_front)):
        segments[f"barrel_{region_name}_left"] = _split_half(
            region, keep_positive_y=False, kerf_mm=kerf
        )
        segments[f"barrel_{region_name}_right"] = _split_half(
            region, keep_positive_y=True, kerf_mm=kerf
        )

    # Receiver body — trim hanging grip and top rail so height fits P1S.
    receiver = build_receiver(params)
    bbox = receiver.val().BoundingBox()
    cx = (bbox.xmin + bbox.xmax) / 2.0
    cy = (bbox.ymin + bbox.ymax) / 2.0

    # Half-space cut: remove everything below Z=0 (hanging grip).
    below = (
        cq.Workplane("XY")
        .workplane(offset=-500.0)
        .center(cx, cy)
        .box(2000.0, 2000.0, 1000.0)
    )
    # Half-space cut: remove everything above receiver roof (rail).
    above = (
        cq.Workplane("XY")
        .workplane(offset=params.receiver_height_mm + 500.0)
        .center(cx, cy)
        .box(2000.0, 2000.0, 1000.0)
    )
    receiver_body = _fuse_solids(receiver.cut(below).cut(above))

    rx0, rx1 = _receiver_x_span(params)
    receiver_mid = (rx0 + rx1) / 2.0
    receiver_rear = _split_along_x(
        receiver_body, cut_x_mm=receiver_mid, keep_positive_x=False, kerf_mm=kerf
    )
    receiver_front = _split_along_x(
        receiver_body, cut_x_mm=receiver_mid, keep_positive_x=True, kerf_mm=kerf
    )
    for region_name, region in (("rear", receiver_rear), ("front", receiver_front)):
        segments[f"receiver_{region_name}_left"] = _split_half(
            region, keep_positive_y=False, kerf_mm=kerf
        )
        segments[f"receiver_{region_name}_right"] = _split_half(
            region, keep_positive_y=True, kerf_mm=kerf
        )

    # Separate grip stub: keep only geometry below Z=0.
    full_receiver = build_receiver(params)
    grip_keep_cutter = (
        cq.Workplane("XY")
        .workplane(offset=500.0)
        .center(cx, cy)
        .box(2000.0, 2000.0, 1000.0)
    )
    grip = _fuse_solids(full_receiver.cut(grip_keep_cutter))
    segments["grip"] = grip

    # Validate each segment fits the configured printer envelope.
    oversized = []
    for name, solid in segments.items():
        validate_model(solid, expected_solid_count=1, min_volume_mm3=10.0)
        if name != "grip" and not _fits_printer(solid, params):
            bb = solid.val().BoundingBox()
            oversized.append(
                f"{name}={bb.xlen:.1f}x{bb.ylen:.1f}x{bb.zlen:.1f}"
            )
    if oversized:
        raise ValueError(
            "P1S segments exceed printer envelope: " + ", ".join(oversized)
        )

    return segments


def build_exploded_assembly(
    params: WaterGunShellParameters | None = None,
    *,
    gap_mm: float = 40.0,
) -> cq.Workplane:
    """Translate P1S segments apart for an exploded visualization compound."""
    params = params or p1s_parameters()
    segments = build_p1s_segments(params)

    # Explode offsets: stock rear, receiver center, barrel forward; L/R apart.
    offsets = {
        "stock_left": (-gap_mm * 2.5, -gap_mm, 0.0),
        "stock_right": (-gap_mm * 2.5, gap_mm, 0.0),
        "receiver_rear_left": (-gap_mm * 0.5, -gap_mm, 0.0),
        "receiver_rear_right": (-gap_mm * 0.5, gap_mm, 0.0),
        "receiver_front_left": (gap_mm * 0.5, -gap_mm, 0.0),
        "receiver_front_right": (gap_mm * 0.5, gap_mm, 0.0),
        "barrel_rear_left": (gap_mm * 2.0, -gap_mm, 0.0),
        "barrel_rear_right": (gap_mm * 2.0, gap_mm, 0.0),
        "barrel_front_left": (gap_mm * 3.5, -gap_mm, 0.0),
        "barrel_front_right": (gap_mm * 3.5, gap_mm, 0.0),
        "grip": (0.0, 0.0, -gap_mm * 1.5),
    }

    solids = []
    for name, solid in segments.items():
        dx, dy, dz = offsets.get(name, (0.0, 0.0, 0.0))
        moved = solid.translate((dx, dy, dz))
        solids.extend(moved.solids().vals())

    if not solids:
        raise ValueError("no segments to explode")
    compound = cq.Compound.makeCompound(solids)
    return cq.Workplane("XY").newObject([compound])


def build_part(params: WaterGunShellParameters | None = None) -> cq.Workplane:
    """Compatibility helper returning the full empty shell."""
    return build_full_shell(params)


def parameters_dict(params: WaterGunShellParameters) -> dict:
    data = asdict(params)
    data["overall_length_mm"] = overall_length_mm(params)
    data["overall_width_mm"] = overall_width_mm(params)
    data["overall_height_mm"] = overall_height_mm(params)
    data["tank_volume_gal_nominal"] = 2.5
    data["tank_reference_inches"] = {
        "spun_approx_l_in": 12.0,
        "spun_approx_d_in": 8.0,
        "length_mm": 12.0 * INCH_TO_MM,
        "diameter_mm": 8.0 * INCH_TO_MM,
    }
    return data


def expected_bbox_full_mm(
    params: WaterGunShellParameters,
) -> tuple[float, float, float]:
    """Loose expected bounding box for the full shell (includes cheek/pad)."""
    length = overall_length_mm(params)
    width = overall_width_mm(params) + 18.0 + 16.0  # cheek plate + stock pad
    height = overall_height_mm(params)
    return (length, width, height)


def export_shell(
    params: WaterGunShellParameters | None = None,
    *,
    stl_quality: str = "normal",
    include_halves: bool = True,
    include_p1s_segments: bool = True,
) -> dict[str, dict[str, Path]]:
    """Validate and export full shell, halves, and optional P1S segments."""
    params = params or WaterGunShellParameters()
    validate_parameters(params)

    outputs: dict[str, dict[str, Path]] = {}

    full = build_full_shell(params)
    validate_model(full, expected_solid_count=1, min_volume_mm3=1000.0)
    outputs["full"] = export_part_formats(
        full,
        product=PRODUCT_NAME,
        part="full",
        variant=VARIANT,
        revision=params.revision,
        stl_quality=stl_quality,
    )

    for module in ("barrel", "receiver", "stock"):
        solid = {
            "barrel": build_barrel,
            "receiver": build_receiver,
            "stock": build_stock,
        }[module](params)
        validate_model(solid, expected_solid_count=1, min_volume_mm3=100.0)
        outputs[module] = export_part_formats(
            solid,
            product=PRODUCT_NAME,
            part=module,
            variant=VARIANT,
            revision=params.revision,
            stl_quality=stl_quality,
        )

        if include_halves:
            halves = build_printable_halves(module, params)
            for side, half in halves.items():
                validate_model(half, expected_solid_count=1, min_volume_mm3=50.0)
                outputs[f"{module}_{side}"] = export_part_formats(
                    half,
                    product=PRODUCT_NAME,
                    part=f"{module}_{side}",
                    variant=VARIANT,
                    revision=params.revision,
                    stl_quality=stl_quality,
                )

    if include_p1s_segments:
        p1s_params = p1s_parameters()
        segments = build_p1s_segments(p1s_params)
        for name, solid in segments.items():
            outputs[f"p1s_{name}"] = export_part_formats(
                solid,
                product=PRODUCT_NAME,
                part=f"p1s_{name}",
                variant="p1s",
                revision=p1s_params.revision,
                stl_quality=stl_quality,
            )
        exploded = build_exploded_assembly(p1s_params, gap_mm=40.0)
        validate_model(
            exploded,
            expected_solid_count=None,
            min_volume_mm3=1000.0,
        )
        outputs["p1s_exploded"] = export_part_formats(
            exploded,
            product=PRODUCT_NAME,
            part="p1s_exploded",
            variant="p1s",
            revision=p1s_params.revision,
            stl_quality=stl_quality,
        )

    return outputs


if __name__ == "__main__":
    parameters = WaterGunShellParameters()
    print(
        "Overall envelope (mm): "
        f"{overall_length_mm(parameters):.1f} L x "
        f"{overall_width_mm(parameters):.1f} W x "
        f"{overall_height_mm(parameters):.1f} H"
    )
    exported = export_shell(parameters, stl_quality="draft")
    for name, paths in exported.items():
        for fmt, path in paths.items():
            print(f"{name}.{fmt}: {path}")

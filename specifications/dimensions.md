# Dimensions — Havoc Water-Gun Empty Shell Rev B

Units: millimeters

Rev B improves component housing vs Rev A: cylindrical tank cradle, stock motor bay,
barrel water-bore + inert LV conduit, hose tunnel, and recessed panel grooves.
Inspired by the Flame V3 1.0 Tinkercad layout (Havoc silhouette / cavity placement).

## Layout

| Region | Parameter | Value | Notes |
|--------|-----------|------:|-------|
| Receiver | receiver_length_mm | 380.0 | Mid-body / tank bay |
| Receiver | receiver_width_mm | 280.0 | Outer width |
| Receiver | receiver_height_mm | 280.0 | Outer height |
| Barrel | barrel_length_mm | 420.0 | Forward of receiver |
| Barrel | barrel_shroud_width_mm | 110.0 | Blocky shroud |
| Barrel | barrel_shroud_height_mm | 110.0 | Tall enough for dual channel |
| Barrel | barrel_bore_diameter_mm | 40.0 | Water-nozzle packing bore |
| Barrel | barrel_conduit_diameter_mm | 18.0 | Inert LV wiring/sensor chase |
| Barrel | barrel_conduit_offset_z_mm | 32.0 | Above bore axis |
| Barrel | barrel_outer_diameter_front_mm | 72.0 | Collar sizing |
| Barrel | barrel_outer_diameter_rear_mm | 92.0 | Collar sizing |
| Stock | stock_length_mm | 200.0 | Rear of receiver |
| Stock | stock_width_mm | 150.0 | Thick stubby stock |
| Stock | stock_height_mm | 170.0 | Motor + battery envelope |
| Wall | wall_thickness_mm | 3.2 | Shell wall |
| Corner | corner_radius_mm | 8.0 | Softened vertical edges |

## Exclusion zones (packing envelopes)

| Zone | Parameter | Value | Notes |
|------|-----------|------:|-------|
| Tank | tank_cavity_length_mm | 330.0 | ~2.5 gal class water reservoir |
| Tank | tank_cavity_width_mm | 220.0 | |
| Tank | tank_cavity_height_mm | 220.0 | |
| Tank | tank_clearance_mm | 10.0 | Added around tank L/W; added to height |
| Tank | tank_cradle_diameter_mm | 210.0 | Spun-style cylindrical cradle |
| H-pump | h_pump_length_mm | 160.0 | Horizontal water-pump footprint |
| H-pump | h_pump_width_mm | 100.0 | |
| H-pump | h_pump_height_mm | 100.0 | |
| V-pump | v_pump_diameter_mm | 100.0 | Vertical water-pump footprint |
| V-pump | v_pump_height_mm | 180.0 | |
| Motor | motor_cavity_length_mm | 95.0 | Stock pump-motor packing |
| Motor | motor_cavity_diameter_mm | 72.0 | |
| Battery | battery_cavity_length_mm | 70.0 | Stock LV bay |
| Battery | battery_cavity_width_mm | 100.0 | |
| Battery | battery_cavity_height_mm | 90.0 | |
| Hose | hose_tunnel_diameter_mm | 28.0 | Receiver→barrel water packing path |

## Cosmetic / detail features

| Feature | Parameter | Value |
|---------|-----------|------:|
| Grip stub | grip_length_mm | 125.0 |
| Grip stub | grip_width_mm | 44.0 |
| Grip stub | grip_height_mm | 120.0 |
| Top rail | rail_width_mm / height_mm | 28.0 / 18.0 |
| Receiver grooves | receiver_side_rib_count | 6 |
| Barrel grooves | barrel_side_rib_count | 8 |

## Safety notes for cavities

- Tank / pump / motor cavities = **water-gun packing envelopes only**
- Barrel bore = water-nozzle path; barrel conduit = **inert low-voltage wiring/sensor chase**
- **Not** fuel, ignition, high-voltage spark, combustion, or flame systems

## Coordinate System

- Origin at geometric center of receiver outer XY envelope
- +X muzzle / barrel, -X stock, +Y right, +Z up
- Z = 0 at exterior bottom of receiver

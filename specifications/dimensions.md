# Dimensions — Havoc Water-Gun Empty Shell Rev A

Units: millimeters

## Layout

| Region | Parameter | Value | Notes |
|--------|-----------|------:|-------|
| Receiver | receiver_length_mm | 380.0 | Mid-body / tank bay (+X forward half) |
| Receiver | receiver_width_mm | 280.0 | Outer width |
| Receiver | receiver_height_mm | 280.0 | Outer height |
| Barrel | barrel_length_mm | 420.0 | Forward of receiver |
| Barrel | barrel_shroud_width_mm | 110.0 | Blocky shroud |
| Barrel | barrel_shroud_height_mm | 100.0 | Blocky shroud |
| Barrel | barrel_bore_diameter_mm | 48.0 | Empty cosmetic bore |
| Barrel | barrel_outer_diameter_front_mm | 72.0 | Collar sizing input |
| Barrel | barrel_outer_diameter_rear_mm | 92.0 | Collar sizing input |
| Stock | stock_length_mm | 200.0 | Rear of receiver |
| Stock | stock_width_mm | 150.0 | Thick stubby stock |
| Stock | stock_height_mm | 170.0 | Battery bay height envelope |
| Wall | wall_thickness_mm | 3.0 | Shell wall |
| Corner | corner_radius_mm | 8.0 | Softened vertical edges |

## Exclusion zones (packing envelopes)

| Zone | Parameter | Value | Notes |
|------|-----------|------:|-------|
| Tank | tank_cavity_length_mm | 330.0 | ~2.5 gal class |
| Tank | tank_cavity_width_mm | 220.0 | |
| Tank | tank_cavity_height_mm | 220.0 | |
| Tank | tank_clearance_mm | 10.0 | Added around tank L/W; added to height |
| H-pump | h_pump_length_mm | 160.0 | Horizontal pump footprint |
| H-pump | h_pump_width_mm | 100.0 | |
| H-pump | h_pump_height_mm | 100.0 | |
| V-pump | v_pump_diameter_mm | 100.0 | Vertical pump footprint |
| V-pump | v_pump_height_mm | 180.0 | |
| Battery | battery_cavity_length_mm | 160.0 | Inside stock |
| Battery | battery_cavity_width_mm | 110.0 | |
| Battery | battery_cavity_height_mm | 130.0 | |

## Cosmetic features

| Feature | Parameter | Value |
|---------|-----------|------:|
| Grip stub | grip_length_mm | 120.0 |
| Grip stub | grip_width_mm | 42.0 |
| Grip stub | grip_height_mm | 115.0 |
| Top rail | rail_length_mm | 260.0 (clamped to forward roof in builder) |
| Top rail | rail_width_mm | 28.0 |
| Top rail | rail_height_mm | 18.0 |

## Print / joint parameters

| Parameter | Value | Notes |
|-----------|------:|-------|
| split_kerf_mm | 0.20 | Left/right half split gap |
| flange_depth_mm | 12.0 | Reserved for future module joints |
| flange_clearance_mm | 0.40 | Reserved for future module joints |

## Coordinate System

- Origin at geometric center of receiver outer XY envelope
- +X muzzle / barrel, -X stock, +Y right, +Z up
- Z = 0 at exterior bottom of receiver

## Reference tank (ASSUMPTION A1)

Common 2.5-gal go-kart spun tank ≈ 12 in length × 8 in diameter
(≈ 304.8 × 203.2 mm). Rectangular plastics are similar. Cavity above is oversized for clearance.

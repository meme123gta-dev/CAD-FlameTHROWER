# Hardware reference — Amazon motor/pump ASIN B07NYZ2CGK

**Role in this repo:** packing / fit-check reference solid for the theatrical
**water-gun** empty shell. Treat as a water/vacuum pump packing model only —
do **not** design fuel, ignition, combustion, or flame systems.

CadQuery source: `src/parts/hardware_motor.py`  
Exports: `exports/stl/hardware_motor_vacuum_pump_b07nyz2cgk_rev_a.stl` (and STEP)

## Source

- URL: https://www.amazon.com/dp/B07NYZ2CGK
- ASIN: **B07NYZ2CGK**
- Captured: 2026-08-07 (live Amazon product page)
- Screenshots: `/opt/cursor/artifacts/amazon_motor_*.webp`

## Listing identity

| Field | Value |
|-------|-------|
| Title | FTVOGUE Oilless Vacuum Pump DC12V 42W Mini Brush Piston Pressure Pump 40L/min |
| Brand | FTVOGUE |
| Model | **VN-C4** |
| Type | Oilless mini diaphragm / piston vacuum pump |
| UPC | 783335735815 |

## Exact seller-listed dimensions

From the product dimension diagram / specs table:

| Spec | Value | Notes |
|------|------:|-------|
| Overall length | **90 mm** | 3.54 in |
| Overall width | **44 mm** | 1.73 in |
| Overall height | **110 mm** | 4.33 in |
| Hose interface diameter | **8 mm** | barb OD for tubing |
| Mass | **488 g** (approx) | 1.1 lb listing weight |

## Electrical / performance (listing)

| Spec | Value |
|------|------:|
| Rated voltage | DC **12 V** |
| Working voltage | DC **9–14 V** |
| Power | **42 W** |
| Flow | **40 L/min** |
| Vacuum | **−85 kPa** |
| Wiring | RED = +12 V, BLACK = GND |

Note: one product-photo label shows “24V”; the listing title/specs say **DC12V**.
Use 12 V as the sales-page rated value; verify on the physical unit label.

## Pickup vs output (port roles)

From the seller **installation diagram** (AIR INLET / AIR OUTLET labels):

| Role | Seller label | Physical location (reference model) | Function |
|------|--------------|-------------------------------------|----------|
| **PICKUP** | **AIR INLET** | Hose barb on pump-head face toward the motor (+X in CadQuery model) | Suction / vacuum (−85 kPa) |
| **OUTPUT** | **AIR OUTLET** | Hose barb on **top** of pump head (+Z) | Discharge / exhaust |

Evidence:
- Installation graphic: connect suction device to **AIR INLET**; exhaust hose to **AIR OUTLET**.
- Close-up listing photos show molded flow arrows on barbs (inward = inlet / pickup, outward = outlet / output) on some units.

**Ambiguity (documented):** some gallery images show four barbs (dual-chamber). The CadQuery reference models the **primary INLET + OUTLET** pair from the installation diagram. Confirm barb count/layout on the physical unit before hard-mounting hoses.

## CadQuery coordinate system (`build_motor`)

- Origin at bottom center of mounting plate
- +X → motor free end; −X → pump-head free end; +Z up
- `port_roles` also stored in `parameters_dict()`

## Assumptions used in the solid (not seller-listed)

| ID | Assumption |
|----|------------|
| M1 | Motor can OD ≈ 42 mm (775-class look in photos) |
| M2 | Pump-head block sized to sit inside the 90×44×110 mm envelope |
| M3 | Mount-hole spacing assumed 70×40 mm — **verify on unit** |
| M4 | Primary INLET/OUTLET pair modeled; dual-chamber extra barbs omitted |

## Safety / scope reminder

- Listing is a lab/medical-style **vacuum pump**, reused here only as a packing
  reference for a theatrical water-gun shell.
- Do not add fuel plumbing, ignition, high-voltage spark, or flame-effect internals.

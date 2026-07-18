# CAD Build Report

## Build

- Timestamp (UTC): 20260718T001347Z
- Git commit: `c093424`
- Product: electronics enclosure
- Revision: A

## Parameters

- Length: 160.00 mm
- Width: 90.00 mm
- Height: 50.00 mm
- Wall thickness: 2.40 mm
- Lid fit clearance: 0.35 mm

## Base

- Solid count: 1
- Volume: 88992.2 mm^3
- Bounding box: 160.00 × 90.00 × 52.50 mm

## Lid

- Solid count: 1
- Volume: 49291.0 mm^3
- Bounding box: 160.00 × 90.00 × 7.20 mm

## Validation

- Solid count: Pass
- Positive volume: Pass
- Bounding dimensions: Pass
- Export presence: Pass

## Exports

- base.step: `exports/step/electronics_enclosure_base_default_rev_a.step`
- base.stl: `exports/stl/electronics_enclosure_base_default_rev_a.stl`
- lid.step: `exports/step/electronics_enclosure_lid_default_rev_a.step`
- lid.stl: `exports/stl/electronics_enclosure_lid_default_rev_a.stl`

## Warnings

- M3 heat-set insert hole diameter is supplier-dependent and must be confirmed.
- PROTOTYPE ONLY — STRUCTURAL CAPACITY NOT VERIFIED
- Lid fit clearance should be verified with a fit-test coupon on the target printer.

## Assumptions

- ASSUMPTION A1: Target process is FDM with a 0.4 mm nozzle.
- ASSUMPTION A2: Default material is PETG unless overridden.
- ASSUMPTION A3: Enclosure is for low-voltage electronics only.

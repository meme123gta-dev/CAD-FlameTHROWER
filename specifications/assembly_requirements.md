# Assembly Requirements — Havoc Water-Gun Empty Shell

## Modules

1. Receiver — houses tank exclusion and pump packing bays; cosmetic grip + rail.
2. Barrel — long hollow shroud with empty bore; mates to receiver +X face.
3. Stock — thick stubby butt with battery/component cavity; mates to receiver -X face.

## Iteration-1 joint intent

Modules are exported as separate solids for printing. Mechanical fasteners, sealing,
and interlocking flanges are **not** finalized. Parameters `flange_depth_mm` and
`flange_clearance_mm` are reserved.

Recommended prototype join (manual):
- Align module end faces
- Use external straps / printed lugs (future revision) or adhesive for display mockups only

## Printable halves

Each module can be split on the Y=0 plane into left/right halves with `split_kerf_mm`.
Print on the flat split face when orientation allows, then join halves along the split.

## Hardware packing (not modeled as solids)

- ~2.5 gal fluid tank into receiver hatch / cavity
- Horizontal pump into forward receiver bay (side access)
- Vertical pump into rear-left receiver bay (side access)
- Batteries / low-voltage electronics into stock cavity (butt + top hatch)

## Exclusions

Do not assemble fuel, ignition, combustion, or pressurized-gas systems into this shell.

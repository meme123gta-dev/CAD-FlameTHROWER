# Part Requirements — Havoc Water-Gun Empty Shell Rev A

## Part Name

Havoc-inspired theatrical water-gun empty shell (barrel + receiver + stock)

## Purpose

Printable exterior enclosure / prop shell for a theatrical or display water-gun build.
The shell provides packing volume for a ~2.5-gallon fluid tank, horizontal and vertical
pump footprints, and a stubby stock bay for batteries / low-voltage components.

## Safe Scope Classification

Permitted:
- Exterior shell modules (barrel shroud, receiver, stock)
- Cosmetic empty bore and grip stub
- Placeholder exclusion cavities for tank and pumps
- Printable left/right halves

Excluded:
- Fuel storage systems, pressurization, ignition, combustion, flame projection
- Weapon functionality, projectile launch systems, or pressurized-gas internals
- Functional pump / plumbing design (cavities are packing envelopes only)

## Overall Dimensions (default)

- Overall length: 1000.0 mm (stock 200 + receiver 380 + barrel 420)
- Overall width: ~280 mm at receiver (cheek plate adds ~15 mm)
- Overall height: ~410 mm including grip stub and top rail

## Maximum Envelope

Approximately 1004 × 295 × 410 mm for the assembled reference solid.

## Mating Components

- Barrel module (hollow shroud)
- Receiver module (tank + dual pump cavities)
- Stock module (battery / component bay)
- Left/right printable halves of each module

## Mounting Method

Iteration 1 is an empty shell only. Mating flanges / fasteners for module joints are
stub parameters (`flange_depth_mm`, `flange_clearance_mm`) reserved for a later revision.

## Material

Default assumption: PETG. PLA acceptable for visual fit prototypes.

## Manufacturing Process

FDM 3D printing. Print left/right halves flat on the split face when possible.

## Printer

Generic FDM; halves target ~220–300 mm bed class. Full modules may require a large bed
or further segmentation in a later revision.

## Nozzle Diameter

0.4 mm

## Expected Loads

Prototype / display handling only. Structural capacity not verified.

## Environmental Conditions

Indoor prototype / display use unless material and sealing are re-specified.
Water contact sealing is out of scope for Rev A.

## Required Clearances

- Tank packing clearance: 10.0 mm around nominal tank exclusion
- Split kerf between halves: 0.20 mm
- Module flange clearance (future): 0.40 mm

## Surface Finish

As-printed FDM; optional light sanding on exterior cosmetic faces.

## Color

Configurable at print time; not encoded in geometry.

## Branding

Silhouette inspired by the Apex Legends Havoc energy AR for proportion only.
Not a licensed replica; names and game IP are not embedded in geometry.

## Export Formats

STEP and STL for:
- full assembled shell (reference)
- barrel / receiver / stock modules
- left and right printable halves of each module

## Known Dimensions

See `dimensions.md` and `WaterGunShellParameters` in `src/parts/water_gun_shell.py`.

## Assumptions

- ASSUMPTION A1: ~2.5 gal go-kart style tank ≈ 12×8 in spun or similar rectangular plastic;
  cavity uses 330 × 220 × 220 mm plus 10 mm clearance.
- ASSUMPTION A2: Horizontal pump footprint ≈ 160 × 100 × 100 mm.
- ASSUMPTION A3: Vertical pump footprint ≈ Ø100 × 180 mm tall.
- ASSUMPTION A4: Stock battery/component bay ≈ 160 × 110 × 130 mm.
- ASSUMPTION A5: Target process is FDM with a 0.4 mm nozzle; default material PETG.
- ASSUMPTION A6: Aesthetic is Havoc-inspired only (long barrel, thick mid-body, stubby stock).

## Unknowns

- Exact Amazon tank SKU outer envelope and fill-cap location
- Exact pump brand / mounting ear pattern
- Battery pack chemistry and connector locations
- Final module joint fasteners and sealing strategy
- Whether a true left/right clam-shell or sectional length split is preferred for production

## Excluded Hazardous Functionality

No fuel, ignition, combustion, pressurized gas, flame-effect internals, or weapon functionality.
Tank cavity is for inert water/fluid theatrical packing only.

## Acceptance Criteria

- Parametric CadQuery source regenerates
- Full shell and each module are valid single solids
- Left/right halves of each module are valid single solids
- STEP and STL export succeed into `exports/`
- Assumptions and revision documented

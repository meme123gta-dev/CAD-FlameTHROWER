# Part Requirements — Havoc Water-Gun Empty Shell Rev B

## Part Name

Havoc-inspired theatrical water-gun empty shell (barrel + receiver + stock)

## Purpose

Printable exterior enclosure / prop shell for a theatrical or display **water-gun** build.
The shell provides packing volume for a ~2.5-gallon **water** reservoir, horizontal and
vertical pump footprints, a stock bay for a water-pump motor + batteries / low-voltage
components, and a barrel with a water-nozzle bore plus an inert LV conduit chase.

Rev B redesign is informed by the user's Flame V3 1.0 Tinkercad layout (component cavity
placement, ribbed/panel language, motor-in-stock) while keeping CadQuery as master source.

## Safe Scope Classification

Permitted:
- Exterior shell modules (barrel shroud, receiver, stock)
- Water-nozzle packing bore and inert low-voltage wiring/sensor conduit
- Placeholder exclusion cavities for water tank, pumps, and pump motor
- Printable left/right halves and P1S segments
- Cosmetic panel grooves, rail, grip, cheek plate

Excluded:
- Fuel storage systems, pressurization for flame effects, ignition, combustion, flame projection
- High-voltage ignition / spark systems in the barrel (conduit is LV/sensor packing only)
- Weapon functionality or projectile launch systems
- Functional sealed pump / plumbing design (cavities are packing envelopes only)

## Overall Dimensions (default)

- Overall length: 1000.0 mm (stock 200 + receiver 380 + barrel 420)
- Overall width: ~280 mm at receiver (cheek plate adds ~15 mm)
- Overall height: ~418 mm including grip stub and top rail

## Mating Components

- Barrel module (water bore + LV conduit + hose dock)
- Receiver module (tank cradle + dual pump cavities + hose tunnel)
- Stock module (motor bay + battery bay)
- Left/right printable halves / P1S segments of each module

## Material

Default assumption: PETG. PLA acceptable for visual fit prototypes.

## Manufacturing Process

FDM 3D printing. Print left/right halves flat on the split face when possible.
P1S segments target Bambu Lab P1S 256³ bed.

## Excluded Hazardous Functionality

No fuel, ignition, combustion, pressurized gas for flame effects, high-voltage spark,
flame-effect internals, or weapon functionality. Tank cavity is for inert water/fluid
theatrical packing only. Barrel “hollow points” from the V3 reference map to water bore
+ inert LV conduit — not ignition hardware.

## Acceptance Criteria

- Parametric CadQuery source regenerates (Rev B)
- Full shell and each module are valid single solids
- Left/right halves and P1S segments are valid single solids
- STEP and STL export succeed into `exports/`
- Assumptions and revision documented
- Tinkercad design **Flame V4 1.0_AI** can import the exploded / module STLs

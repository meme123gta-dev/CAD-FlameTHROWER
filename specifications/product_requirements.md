# Part Requirements

## Part Name

Low-voltage electronics enclosure (base + lid)

## Purpose

Protective two-piece housing for low-voltage control electronics, connectors, and cable routing in consumer product prototypes and display mockups.

## Safe Scope Classification

Permitted: exterior shell, lid, mounting bosses for heat-set inserts, cable-entry opening for low-voltage wiring, alignment features, cosmetic rounded corners.

Excluded: fuel storage, pressurization, ignition, combustion, flame projection, pressure vessels, burner/nozzle geometry, or any weapon-related functionality.

## Overall Dimensions

- Length: 160.0 mm
- Width: 90.0 mm
- Height (base): 50.0 mm
- Lid thickness: 3.2 mm

## Maximum Envelope

160 × 90 × 57.2 mm assembled without explode gap (base height + lid thickness; pins nest into lid).

## Mating Components

- Enclosure base
- Enclosure lid
- M3 screws into heat-set inserts
- Optional low-voltage cable through side port

## Mounting Method

Four M3 heat-set insert bosses in the base; counterbored clearance holes in the lid.

## Material

Default assumption: PETG. PLA acceptable for visual prototypes.

## Manufacturing Process

FDM 3D printing

## Printer

Generic FDM, 0.4 mm nozzle

## Nozzle Diameter

0.4 mm

## Expected Loads

Prototype handling loads only. Structural capacity not verified.

## Environmental Conditions

Indoor prototype / display use unless material and sealing are re-specified.

## Required Clearances

- Lid fit clearance: 0.35 mm
- Alignment socket clearance: 0.25 mm radial

## Surface Finish

As-printed FDM; optional light sanding on exterior cosmetic faces.

## Color

Configurable at print time; not encoded in geometry.

## Branding

None in Rev A.

## Export Formats

STEP and STL for base and lid.

## Known Dimensions

See `dimensions.md` and `EnclosureParameters` in `src/parts/enclosure.py`.

## Assumptions

- ASSUMPTION A1: Target process is FDM with a 0.4 mm nozzle.
- ASSUMPTION A2: Default material is PETG.
- ASSUMPTION A3: M3 heat-set insert hole diameter 4.2 mm is a starting value and supplier-dependent.

## Unknowns

- Exact PCB outline and connector locations
- Final insert brand / datasheet hole size
- Target printer shrinkage calibration

## Excluded Hazardous Functionality

No fuel, ignition, combustion, pressurized gas, flame-effect internals, or weapon functionality.

## Acceptance Criteria

- Parametric CadQuery source regenerates
- Base and lid are valid single solids
- STEP and STL export succeed
- Bounding-box tests pass
- Assumptions and revision documented

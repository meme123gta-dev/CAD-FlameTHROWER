# Assembly Notes

## Modules

1. Print left/right halves for receiver, barrel, and stock (or full modules on a large bed).
2. Join halves along the split plane (tape/adhesive for mockups; fasteners TBD).
3. Align barrel to receiver +X face and stock to receiver -X face.
4. Pack inert hardware into exclusion cavities:
   - Tank through receiver top hatch
   - Horizontal pump via forward side access
   - Vertical pump via rear-left side access
   - Batteries / low-voltage electronics via stock butt / top hatch

## Exploded preview

Use `src/assemblies/main_assembly.py` for a colored CadQuery assembly of the three modules.

## Exclusions

Do not install fuel, ignition, combustion, or pressurized-gas systems.

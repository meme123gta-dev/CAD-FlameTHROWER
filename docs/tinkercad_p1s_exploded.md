# Bambu Lab P1S print kit + Tinkercad exploded layout

## Printer target

Bambu Lab **P1S** build volume: **256 × 256 × 256 mm**.

Previous left/right module halves were too long/tall for the P1S. Rev A now
exports **P1S segments** that each fit the bed (any orientation).

## Files to import in Tinkercad (exploded assembly)

Folder: `exports/stl/`

Import these into **one** new 3D Design (mm units):

| Order | File | Role |
|------:|------|------|
| 1 | `havoc_water_gun_shell_p1s_exploded_p1s_rev_b.stl` | Optional single-file exploded preview |
| 2 | `havoc_water_gun_shell_full_default_rev_b.stl` | Assembled Rev B reference shell |
| 3 | `havoc_water_gun_shell_p1s_stock_left_p1s_rev_b.stl` | Stock L |
| 4 | `havoc_water_gun_shell_p1s_stock_right_p1s_rev_b.stl` | Stock R |
| 5 | `havoc_water_gun_shell_p1s_receiver_rear_left_p1s_rev_b.stl` | Receiver rear L |
| 6 | `havoc_water_gun_shell_p1s_receiver_rear_right_p1s_rev_b.stl` | Receiver rear R |
| 7 | `havoc_water_gun_shell_p1s_receiver_front_left_p1s_rev_b.stl` | Receiver front L |
| 8 | `havoc_water_gun_shell_p1s_receiver_front_right_p1s_rev_b.stl` | Receiver front R |
| 9 | `havoc_water_gun_shell_p1s_barrel_rear_left_p1s_rev_b.stl` | Barrel rear L |
| 10 | `havoc_water_gun_shell_p1s_barrel_rear_right_p1s_rev_b.stl` | Barrel rear R |
| 11 | `havoc_water_gun_shell_p1s_barrel_front_left_p1s_rev_b.stl` | Barrel front L / muzzle |
| 12 | `havoc_water_gun_shell_p1s_barrel_front_right_p1s_rev_b.stl` | Barrel front R / muzzle |
| 13 | `havoc_water_gun_shell_p1s_grip_p1s_rev_b.stl` | Grip stub (optional separate print) |

## Fast path (one import)

1. Open (or create) the Tinkercad 3D Design named **`Flame V4 1.0_AI`**
   (renamed from `Super Jarv` / `Flame V4 1.0`; older exploded preview may live in `Flame V3 1.0`)
2. **Import** → choose the Rev B exploded or full shell STL:
   - `exports/stl/havoc_water_gun_shell_p1s_exploded_p1s_rev_b.stl` (exploded P1S kit preview)
   - `exports/stl/havoc_water_gun_shell_full_default_rev_b.stl` (assembled reference)
   Absolute paths under the repo `exports/stl/` folder.
3. If prompted about size, keep scale at **100%** (model is already mm). If Tinkercad caps the workplane, scale to **50%** for viewing only — print the individual `p1s_*` segment STLs at **100%** in Bambu Studio.

Safety reminder: this is an **empty theatrical/display water-gun shell** only (no fuel, ignition, HV spark, or flame systems). Barrel hollows are water-nozzle bore + inert LV conduit.

## How pieces sit together

```text
[-X stock] [receiver rear] [receiver front] [barrel rear] [barrel front +X]
   L / R         L / R            L / R           L / R          L / R
                              grip below receiver
```

- **Left** halves mate to **right** halves on the center plane (Y=0).
- **Rear** segments mate to **front** segments on mid-module cut planes.
- Keep each part’s rotation as imported; only slide them together along X/Y to assemble.

## Print in Bambu Studio (P1S)

Import the individual `p1s_*` segment STLs (not the exploded preview) into Bambu Studio,
select printer **Bambu Lab P1S**, and slice one segment per plate (or pack multiple if they fit).

Suggested PETG, 0.4 mm nozzle, 3–4 walls for a large hollow shell prototype.

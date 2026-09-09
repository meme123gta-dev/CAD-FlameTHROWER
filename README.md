# CAD — Havoc Water-Gun Empty Shell

Parametric **CadQuery** workspace for a theatrical/display **water-gun empty shell**
inspired by the Havoc energy AR silhouette (long barrel, thick mid-body, stubby stock).

The editable Python source is the master design file. STEP/STL exports are generated outputs.

## Safety scope

This repository models **exterior shell and inert packing cavities only**.

It **must not** contain designs for functional fuel storage, pressurization, ignition,
combustion, flame projection, or weapon systems.

Tank and pump regions are empty exclusion zones sized for water/fluid theatrical hardware packing.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Build + validate empty shell
python scripts/build_all.py
python scripts/validate_all.py

# Export STEP + STL (full, modules, left/right halves)
python scripts/export_all.py

# Run tests
pytest

# Export Amazon tank + motor reference solids (for Tinkercad / fit checks)
python scripts/export_hardware.py
```

### Virtual environment notes

- Use Python 3.10+.
- On Debian/Ubuntu, install `python3-venv` first if needed (`sudo apt install python3.12-venv`).
- CadQuery pulls native OCP dependencies; confirm with:
  `python -c "import cadquery as cq; print(cq.__version__)"`

## Primary part — water-gun empty shell Rev A

Three modules plus printable halves:

| Module | Role |
|--------|------|
| Receiver | Tank bay + horizontal/vertical pump packing cavities |
| Barrel | Long hollow shroud with empty cosmetic bore |
| Stock | Thick stubby stock with battery/component bay |

Source: `src/parts/water_gun_shell.py`

Default printable STLs (after export):

- `exports/stl/havoc_water_gun_shell_full_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_receiver_left_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_receiver_right_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_barrel_left_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_barrel_right_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_stock_left_default_rev_a.stl`
- `exports/stl/havoc_water_gun_shell_stock_right_default_rev_a.stl`

(Plus matching STEP files under `exports/step/`.)

## Envelope (default)

- Length ≈ 1000 mm (200 stock + 380 receiver + 420 barrel)
- Width ≈ 280 mm at receiver
- Height ≈ 410 mm including grip stub and top rail
- Tank cavity ≈ 330 × 220 × 220 mm + 10 mm clearance (~2.5 gal class)

## Repository layout

```text
.
├── config/                 # materials, printers, tolerances, export settings
├── specifications/         # requirements, dimensions, revisions
├── src/
│   ├── common/             # helpers, fasteners, validation, exporters
│   ├── parts/              # parametric parts (water_gun_shell primary)
│   ├── assemblies/         # assembly composition
│   └── variants/           # size/style variants
├── tests/                  # geometry, dimensions, clearances, exports
├── exports/                # generated STEP/STL/etc. (not source of truth)
├── scripts/                # build / validate / export / report
└── docs/                   # manufacturing, assembly, inspection notes
```

## Common commands

| Command | Purpose |
|---------|---------|
| `python scripts/build_all.py` | Regenerate solids and validate |
| `python scripts/validate_all.py` | Geometry/envelope checks |
| `python scripts/export_all.py` | Write STEP + STL + build report |
| `python scripts/generate_report.py` | Write build report only |
| `pytest` | Run automated tests |
| `ruff check .` | Lint |
| `black .` | Format |

## Design rules (short)

- Named parameters with units; no unexplained magic numbers
- Validate parameters before building
- Prefer reusable helpers in `src/common/`
- Keep exports deterministic and revisioned
- Document assumptions and unknowns
- Human review required before production use

## Status

Rev A empty shell is an **iteration-1 prototype** for silhouette and packing volume.

**PROTOTYPE ONLY — STRUCTURAL CAPACITY NOT VERIFIED**

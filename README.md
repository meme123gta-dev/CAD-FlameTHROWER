# CAD-FlameTHROWER / Startup CAD Workspace

Parametric **CadQuery** workspace for 3D-printed consumer product housings, fixtures, mounts, display models, and other **safe** mechanical components.

The editable Python source is the master design file. STEP/STL exports are generated outputs.

## Safety scope

This repository may support exterior/cosmetic work related to theatrical or demonstration equipment, but it **must not** contain designs for functional fuel storage, pressurization, ignition, combustion, flame projection, or weapon systems.

The sample part included here is a **low-voltage electronics enclosure** only.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Build + validate sample enclosure
python scripts/build_all.py
python scripts/validate_all.py

# Export STEP + STL
python scripts/export_all.py

# Run tests
pytest
```

### Virtual environment notes

- Use Python 3.10+.
- On Debian/Ubuntu, install `python3-venv` first if `python3 -m venv` fails (`sudo apt install python3.12-venv`).
- Activate with `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows).
- CadQuery pulls native OCP dependencies; if installation fails, capture the pip error and retry on a supported platform/architecture.
- After install, confirm with: `python -c "import cadquery as cq; print(cq.__version__)"`

## Sample part — electronics enclosure Rev A

Two-piece enclosure with:

- Rounded outer corners
- Removable lid with nesting lip
- M3 heat-set insert bosses in the base
- Counterbored M3 clearance holes in the lid
- Low-voltage cable-entry opening
- Alignment pins/sockets
- Configurable fit clearances

Source: `src/parts/enclosure.py`

Default exports:

- `exports/step/electronics_enclosure_base_default_rev_a.step`
- `exports/step/electronics_enclosure_lid_default_rev_a.step`
- `exports/stl/electronics_enclosure_base_default_rev_a.stl`
- `exports/stl/electronics_enclosure_lid_default_rev_a.stl`

## Repository layout

```text
.
├── config/                 # materials, printers, tolerances, export settings
├── specifications/         # requirements, dimensions, revisions
├── src/
│   ├── common/             # helpers, fasteners, validation, exporters
│   ├── parts/              # parametric parts (enclosure sample)
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

Rev A sample enclosure is a **prototype workflow demonstrator**.

**PROTOTYPE ONLY — STRUCTURAL CAPACITY NOT VERIFIED**

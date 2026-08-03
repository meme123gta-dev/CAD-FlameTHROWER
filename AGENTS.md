# AGENTS.md

## Cursor Cloud specific instructions

This is a parametric **CadQuery** (Python) CAD workspace. The "application" is a set of
command-line scripts that build parametric solids, validate their geometry, and export
STEP/STL files. There is no server or GUI to run. See `README.md` for the full command
reference and repository layout.

### Environment

- Python 3.12 with a virtualenv at `.venv/` (the update script creates it and installs
  `requirements.txt`). Activate with `source .venv/bin/activate`, or call tools directly
  via `.venv/bin/<tool>`.
- `cadquery` pulls large native OCP wheels (`cadquery-ocp`, `vtk`). No extra system
  packages are needed for the headless build/validate/export/test pipeline — it imports
  and runs without a display.

### Running the pipeline (all commands from repo root, venv active)

- Build + validate: `python scripts/build_all.py`
- Geometry/envelope checks: `python scripts/validate_all.py`
- Export STEP + STL + build report: `python scripts/export_all.py`
- Tests: `pytest`
- Lint: `ruff check .`
- Format check: `black --check .`

### Non-obvious notes

- Running `python scripts/export_all.py` (or `build_all.py`) rewrites tracked outputs
  under `exports/` and `reports/` and also writes new timestamped
  `reports/build_report_*.md/.json` files. These are generated artifacts, not source. If
  you only ran the pipeline to verify the environment, revert them (`git checkout --
  exports reports` and delete any new timestamped report files) so the working tree stays
  clean.
- `black --check .` currently reports a handful of already-committed files as needing
  reformatting. This is the repo's existing state, not an environment problem — do not
  reformat those files unless the task is specifically about formatting. `ruff check .`
  passes cleanly.
- The master design source is the CadQuery Python code in `src/`; STEP/STL files in
  `exports/` are outputs and are never the source of truth.

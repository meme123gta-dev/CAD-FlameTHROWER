#!/usr/bin/env python3
"""Export STEP and STL files for all sample parts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_all import build_all  # noqa: E402
from scripts.generate_report import write_build_report  # noqa: E402
from src.parts.enclosure import EnclosureParameters, export_enclosure  # noqa: E402


def main() -> int:
    params = EnclosureParameters()
    build_result = build_all(params)
    exports = export_enclosure(params, stl_quality="normal")

    report_path = write_build_report(
        params=params,
        base_validation=build_result["base_validation"],
        lid_validation=build_result["lid_validation"],
        exports=exports,
    )

    print("Export succeeded.")
    for part_name, paths in exports.items():
        for fmt, path in paths.items():
            print(f"  {part_name}.{fmt}: {path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

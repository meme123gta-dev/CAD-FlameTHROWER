#!/usr/bin/env python3
"""Export STEP and STL files for the water-gun empty shell."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_all import build_all  # noqa: E402
from scripts.generate_report import write_build_report  # noqa: E402
from src.parts.water_gun_shell import WaterGunShellParameters, export_shell  # noqa: E402


def main() -> int:
    params = WaterGunShellParameters()
    build_result = build_all(params)
    exports = export_shell(params, stl_quality="normal", include_halves=True)

    report_path = write_build_report(
        params=params,
        validations=build_result["validations"],
        exports=exports,
        envelope_mm=build_result["envelope_mm"],
    )

    print("Export succeeded.")
    for part_name, paths in exports.items():
        for fmt, path in paths.items():
            print(f"  {part_name}.{fmt}: {path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

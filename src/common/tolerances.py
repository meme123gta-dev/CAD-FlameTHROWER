"""Tolerance and fit helpers loaded from project configuration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.common.constants import (
    DEFAULT_GENERAL_CLEARANCE_MM,
    DEFAULT_INSERT_CLEARANCE_MM,
    DEFAULT_LID_FIT_CLEARANCE_MM,
    DEFAULT_MIN_WALL_MM,
    DEFAULT_PRESS_FIT_OFFSET_MM,
    DEFAULT_SCREW_CLEARANCE_MM,
    DEFAULT_SLIDING_CLEARANCE_MM,
    DEFAULT_STRUCTURAL_WALL_MM,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOLERANCES_PATH = PROJECT_ROOT / "config" / "tolerances.json"


@dataclass(frozen=True)
class ToleranceSet:
    general_clearance_mm: float = DEFAULT_GENERAL_CLEARANCE_MM
    sliding_clearance_mm: float = DEFAULT_SLIDING_CLEARANCE_MM
    lid_fit_clearance_mm: float = DEFAULT_LID_FIT_CLEARANCE_MM
    press_fit_offset_mm: float = DEFAULT_PRESS_FIT_OFFSET_MM
    screw_clearance_mm: float = DEFAULT_SCREW_CLEARANCE_MM
    insert_clearance_mm: float = DEFAULT_INSERT_CLEARANCE_MM
    min_wall_mm: float = DEFAULT_MIN_WALL_MM
    structural_wall_mm: float = DEFAULT_STRUCTURAL_WALL_MM


def load_tolerances(path: Path | None = None) -> ToleranceSet:
    """Load tolerance defaults from config/tolerances.json when available."""
    config_path = path or TOLERANCES_PATH
    if not config_path.exists():
        return ToleranceSet()

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    defaults = payload.get("defaults", {})
    return ToleranceSet(
        general_clearance_mm=float(
            defaults.get("general_clearance_mm", DEFAULT_GENERAL_CLEARANCE_MM)
        ),
        sliding_clearance_mm=float(
            defaults.get("sliding_clearance_mm", DEFAULT_SLIDING_CLEARANCE_MM)
        ),
        lid_fit_clearance_mm=float(
            defaults.get("lid_fit_clearance_mm", DEFAULT_LID_FIT_CLEARANCE_MM)
        ),
        press_fit_offset_mm=float(
            defaults.get("press_fit_offset_mm", DEFAULT_PRESS_FIT_OFFSET_MM)
        ),
        screw_clearance_mm=float(
            defaults.get("screw_clearance_mm", DEFAULT_SCREW_CLEARANCE_MM)
        ),
        insert_clearance_mm=float(
            defaults.get("insert_clearance_mm", DEFAULT_INSERT_CLEARANCE_MM)
        ),
        min_wall_mm=float(defaults.get("min_wall_mm", DEFAULT_MIN_WALL_MM)),
        structural_wall_mm=float(
            defaults.get("structural_wall_mm", DEFAULT_STRUCTURAL_WALL_MM)
        ),
    )

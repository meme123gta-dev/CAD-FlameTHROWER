"""Deterministic STEP/STL export helpers."""

from __future__ import annotations

import json
from pathlib import Path

import cadquery as cq

from src.common.constants import (
    EXPORT_TOLERANCE_DRAFT_MM,
    EXPORT_TOLERANCE_FINE_MM,
    EXPORT_TOLERANCE_NORMAL_MM,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPORTS_ROOT = PROJECT_ROOT / "exports"
EXPORT_SETTINGS_PATH = PROJECT_ROOT / "config" / "export_settings.json"

STL_TOLERANCES_MM = {
    "draft": EXPORT_TOLERANCE_DRAFT_MM,
    "normal": EXPORT_TOLERANCE_NORMAL_MM,
    "fine": EXPORT_TOLERANCE_FINE_MM,
}


def load_export_settings(path: Path | None = None) -> dict:
    config_path = path or EXPORT_SETTINGS_PATH
    if not config_path.exists():
        return {
            "stl": {"default_quality": "normal", "tolerances_mm": STL_TOLERANCES_MM}
        }
    return json.loads(config_path.read_text(encoding="utf-8"))


def build_export_stem(
    *,
    product: str,
    part: str,
    variant: str,
    revision: str,
) -> str:
    """Return a deterministic export filename stem."""
    return f"{product}_{part}_{variant}_rev_{revision}".lower()


def ensure_export_dirs() -> dict[str, Path]:
    paths = {
        "step": EXPORTS_ROOT / "step",
        "stl": EXPORTS_ROOT / "stl",
        "3mf": EXPORTS_ROOT / "3mf",
        "dxf": EXPORTS_ROOT / "dxf",
        "drawings": EXPORTS_ROOT / "drawings",
        "previews": EXPORTS_ROOT / "previews",
    }
    for directory in paths.values():
        directory.mkdir(parents=True, exist_ok=True)
    return paths


def export_step(model: cq.Workplane, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(model, str(path))
    if not path.exists() or path.stat().st_size <= 0:
        raise RuntimeError(f"STEP export failed or empty: {path}")
    return path


def export_stl(
    model: cq.Workplane,
    path: Path,
    *,
    quality: str = "normal",
) -> Path:
    settings = load_export_settings()
    tolerances = settings.get("stl", {}).get("tolerances_mm", STL_TOLERANCES_MM)
    tolerance_mm = float(tolerances.get(quality, STL_TOLERANCES_MM["normal"]))

    path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(
        model,
        str(path),
        exportType="STL",
        tolerance=tolerance_mm,
        angularTolerance=0.1,
    )
    if not path.exists() or path.stat().st_size <= 0:
        raise RuntimeError(f"STL export failed or empty: {path}")
    return path


def export_part_formats(
    model: cq.Workplane,
    *,
    product: str,
    part: str,
    variant: str,
    revision: str,
    stl_quality: str | None = None,
) -> dict[str, Path]:
    """Export STEP and STL using the project naming convention."""
    dirs = ensure_export_dirs()
    settings = load_export_settings()
    quality = stl_quality or settings.get("stl", {}).get("default_quality", "normal")
    stem = build_export_stem(
        product=product,
        part=part,
        variant=variant,
        revision=revision,
    )

    step_path = export_step(model, dirs["step"] / f"{stem}.step")
    stl_path = export_stl(model, dirs["stl"] / f"{stem}.stl", quality=quality)
    return {"step": step_path, "stl": stl_path}

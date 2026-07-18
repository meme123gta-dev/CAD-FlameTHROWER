"""Geometry validation helpers for CadQuery solids."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BoundingBoxResult:
    xlen_mm: float
    ylen_mm: float
    zlen_mm: float
    xmin_mm: float
    xmax_mm: float
    ymin_mm: float
    ymax_mm: float
    zmin_mm: float
    zmax_mm: float


@dataclass(frozen=True)
class ValidationResult:
    solid_count: int
    volume_mm3: float
    bounding_box: BoundingBoxResult
    warnings: list[str]


def get_solids(model: cq.Workplane) -> list:
    return model.solids().vals()


def measure_bounding_box(model: cq.Workplane) -> BoundingBoxResult:
    bbox = model.val().BoundingBox()
    return BoundingBoxResult(
        xlen_mm=bbox.xlen,
        ylen_mm=bbox.ylen,
        zlen_mm=bbox.zlen,
        xmin_mm=bbox.xmin,
        xmax_mm=bbox.xmax,
        ymin_mm=bbox.ymin,
        ymax_mm=bbox.ymax,
        zmin_mm=bbox.zmin,
        zmax_mm=bbox.zmax,
    )


def validate_model(
    model: cq.Workplane,
    *,
    expected_solid_count: int | None = 1,
    min_volume_mm3: float = 1.0,
    expected_bbox_mm: tuple[float, float, float] | None = None,
    bbox_tolerance_mm: float = 0.05,
) -> ValidationResult:
    """Validate solid count, volume, and optional bounding-box targets."""
    solids = get_solids(model)
    warnings: list[str] = []

    if not solids:
        raise ValueError("Model contains no solids")

    if expected_solid_count is not None and len(solids) != expected_solid_count:
        raise ValueError(
            f"Expected {expected_solid_count} solid(s), found {len(solids)}"
        )

    total_volume = 0.0
    for index, solid in enumerate(solids):
        volume = float(solid.Volume())
        if volume <= 0:
            raise ValueError(f"Solid {index} has invalid volume: {volume}")
        total_volume += volume

    if total_volume < min_volume_mm3:
        raise ValueError(
            f"Total volume {total_volume:.3f} mm^3 is below minimum {min_volume_mm3}"
        )

    bbox = measure_bounding_box(model)
    if expected_bbox_mm is not None:
        expected_x, expected_y, expected_z = expected_bbox_mm
        checks = (
            ("X", bbox.xlen_mm, expected_x),
            ("Y", bbox.ylen_mm, expected_y),
            ("Z", bbox.zlen_mm, expected_z),
        )
        for axis, actual, expected in checks:
            if abs(actual - expected) > bbox_tolerance_mm:
                raise ValueError(
                    f"Bounding box {axis} length {actual:.3f} mm "
                    f"differs from expected {expected:.3f} mm "
                    f"(tol={bbox_tolerance_mm})"
                )

    if bbox.xlen_mm <= 0 or bbox.ylen_mm <= 0 or bbox.zlen_mm <= 0:
        raise ValueError("Bounding box has a non-positive dimension")

    return ValidationResult(
        solid_count=len(solids),
        volume_mm3=total_volume,
        bounding_box=bbox,
        warnings=warnings,
    )


def assert_within_envelope(
    model: cq.Workplane,
    max_length_mm: float,
    max_width_mm: float,
    max_height_mm: float,
) -> None:
    """Raise if the model exceeds a maximum envelope."""
    bbox = measure_bounding_box(model)
    if bbox.xlen_mm > max_length_mm + 1e-6:
        raise ValueError(
            f"Length {bbox.xlen_mm:.3f} exceeds envelope {max_length_mm:.3f}"
        )
    if bbox.ylen_mm > max_width_mm + 1e-6:
        raise ValueError(
            f"Width {bbox.ylen_mm:.3f} exceeds envelope {max_width_mm:.3f}"
        )
    if bbox.zlen_mm > max_height_mm + 1e-6:
        raise ValueError(
            f"Height {bbox.zlen_mm:.3f} exceeds envelope {max_height_mm:.3f}"
        )

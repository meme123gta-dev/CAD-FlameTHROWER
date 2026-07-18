"""Product variants for the sample electronics enclosure."""

from __future__ import annotations

from src.parts.enclosure import EnclosureParameters


def default_enclosure() -> EnclosureParameters:
    return EnclosureParameters()


def compact_enclosure() -> EnclosureParameters:
    """Smaller envelope for dense low-voltage boards."""
    return EnclosureParameters(
        length_mm=120.0,
        width_mm=70.0,
        height_mm=40.0,
        cable_port_width_mm=12.0,
        cable_port_height_mm=7.0,
    )


def tall_enclosure() -> EnclosureParameters:
    """Taller variant for stacked low-voltage modules."""
    return EnclosureParameters(
        length_mm=160.0,
        width_mm=90.0,
        height_mm=70.0,
        boss_height_mm=12.0,
    )


VARIANTS: dict[str, EnclosureParameters] = {
    "default": default_enclosure(),
    "compact": compact_enclosure(),
    "tall": tall_enclosure(),
}


def get_variant(name: str) -> EnclosureParameters:
    key = name.lower().strip()
    if key not in VARIANTS:
        known = ", ".join(sorted(VARIANTS))
        raise KeyError(f"Unknown variant '{name}'. Known variants: {known}")
    return VARIANTS[key]

"""Product variants for the Havoc water-gun empty shell."""

from __future__ import annotations

from src.parts.water_gun_shell import WaterGunShellParameters, p1s_parameters


def default_shell() -> WaterGunShellParameters:
    return WaterGunShellParameters()


def compact_shell() -> WaterGunShellParameters:
    """Slightly smaller envelope for fit studies on mid-size printers."""
    return WaterGunShellParameters(
        receiver_length_mm=340.0,
        receiver_width_mm=250.0,
        receiver_height_mm=250.0,
        barrel_length_mm=360.0,
        stock_length_mm=180.0,
        stock_width_mm=140.0,
        stock_height_mm=150.0,
        tank_cavity_length_mm=290.0,
        tank_cavity_width_mm=200.0,
        tank_cavity_height_mm=190.0,
        tank_cradle_diameter_mm=190.0,
        battery_cavity_length_mm=60.0,
        battery_cavity_width_mm=90.0,
        battery_cavity_height_mm=80.0,
        motor_cavity_length_mm=85.0,
        motor_cavity_diameter_mm=65.0,
    )


def long_barrel_shell() -> WaterGunShellParameters:
    """Longer barrel shroud for silhouette studies."""
    return WaterGunShellParameters(barrel_length_mm=520.0)


def p1s_shell() -> WaterGunShellParameters:
    """Bambu Lab P1S-oriented envelope (use with build_p1s_segments)."""
    return p1s_parameters()


VARIANTS: dict[str, WaterGunShellParameters] = {
    "default": default_shell(),
    "compact": compact_shell(),
    "long_barrel": long_barrel_shell(),
    "p1s": p1s_shell(),
}


def get_variant(name: str) -> WaterGunShellParameters:
    key = name.lower().strip()
    if key not in VARIANTS:
        known = ", ".join(sorted(VARIANTS))
        raise KeyError(f"Unknown variant '{name}'. Known variants: {known}")
    return VARIANTS[key]

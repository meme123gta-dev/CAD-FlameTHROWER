"""Export path and file generation tests."""

from __future__ import annotations

from pathlib import Path

from src.common.exporters import build_export_stem, export_part_formats
from src.parts.water_gun_shell import WaterGunShellParameters, build_receiver, export_shell


def test_export_stem_naming():
    stem = build_export_stem(
        product="havoc_water_gun_shell",
        part="receiver_left",
        variant="default",
        revision="a",
    )
    assert stem == "havoc_water_gun_shell_receiver_left_default_rev_a"


def test_export_shell_writes_step_and_stl():
    params = WaterGunShellParameters()
    outputs = export_shell(params, stl_quality="draft", include_halves=True)

    required = (
        "full",
        "barrel",
        "receiver",
        "stock",
        "barrel_left",
        "barrel_right",
        "receiver_left",
        "receiver_right",
        "stock_left",
        "stock_right",
    )
    for part_name in required:
        step_path = outputs[part_name]["step"]
        stl_path = outputs[part_name]["stl"]
        assert step_path.exists()
        assert stl_path.exists()
        assert step_path.stat().st_size > 0
        assert stl_path.stat().st_size > 0
        assert step_path.suffix == ".step"
        assert stl_path.suffix == ".stl"


def test_export_part_formats_creates_files():
    model = build_receiver(WaterGunShellParameters())
    paths = export_part_formats(
        model,
        product="havoc_water_gun_shell",
        part="receiver",
        variant="default",
        revision="a",
        stl_quality="draft",
    )
    assert Path(paths["step"]).exists()
    assert Path(paths["stl"]).exists()

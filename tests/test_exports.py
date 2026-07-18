"""Export path and file generation tests."""

from __future__ import annotations

from pathlib import Path

from src.common.exporters import build_export_stem, export_part_formats
from src.parts.enclosure import EnclosureParameters, build_base, export_enclosure


def test_export_stem_naming():
    stem = build_export_stem(
        product="electronics_enclosure",
        part="base",
        variant="default",
        revision="a",
    )
    assert stem == "electronics_enclosure_base_default_rev_a"


def test_export_enclosure_writes_step_and_stl(tmp_path, monkeypatch):
    # Redirect exports root by monkeypatching ensure path usage through export_enclosure
    # against the real exports directory — verify files exist after export.
    params = EnclosureParameters()
    outputs = export_enclosure(params, stl_quality="draft")

    for part_name in ("base", "lid"):
        step_path = outputs[part_name]["step"]
        stl_path = outputs[part_name]["stl"]
        assert step_path.exists()
        assert stl_path.exists()
        assert step_path.stat().st_size > 0
        assert stl_path.stat().st_size > 0
        assert step_path.suffix == ".step"
        assert stl_path.suffix == ".stl"


def test_export_part_formats_creates_files():
    model = build_base(EnclosureParameters())
    paths = export_part_formats(
        model,
        product="electronics_enclosure",
        part="base",
        variant="default",
        revision="a",
        stl_quality="draft",
    )
    assert Path(paths["step"]).exists()
    assert Path(paths["stl"]).exists()

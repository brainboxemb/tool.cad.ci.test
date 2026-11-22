"""Synthetic nested consumer cadquery."""

from __future__ import annotations

import os
from pathlib import Path


item = Path(__file__).parent
repo = Path(os.environ["CAD_CI_REPO"])
output = Path(os.environ["CAD_CI_OUTPUT"])
output.mkdir(parents=True, exist_ok=True)
contract = (item.parent / "verification" / "reference_geometry.json").read_text(
    encoding="utf-8"
)
(output / "result.txt").write_text(
    "cadquery:" + (repo / "shared.txt").read_text(encoding="utf-8") + contract,
    encoding="utf-8",
)

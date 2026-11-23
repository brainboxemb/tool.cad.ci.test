#!/usr/bin/env python3
"""Minimal black-box marker builder for targeted-selection acceptance."""

from pathlib import Path
import os

fixture = Path("fixture.txt").read_text(encoding="utf-8").strip()
item = os.environ["CAD_CI_ITEM"]
if fixture == "fail":
    raise RuntimeError(f"{item}: fixture is configured to fail if selected")

output = Path(os.environ["CAD_CI_OUTPUT"])
output.mkdir(parents=True, exist_ok=True)
(output / "marker.txt").write_text(item + "\n", encoding="utf-8")
print(f"TARGETED_SELECTION_MARKER item={item}", flush=True)

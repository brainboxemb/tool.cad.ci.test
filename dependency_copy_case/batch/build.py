"""Produce one shared result tree for dependency-copy acceptance."""

import os
from pathlib import Path


root = Path(os.environ["CAD_CI_OUTPUT"]) / "items"
value = Path(__file__).with_name("input.txt").read_text(encoding="utf-8")

for name in ("consumer-a", "consumer-b"):
    target = root / name
    (target / "generated").mkdir(parents=True, exist_ok=True)
    (target / "result.txt").write_text(
        f"{name}:{value}",
        encoding="utf-8",
    )
    (target / "generated" / "value.txt").write_text(
        f"{name}-generated:{value}",
        encoding="utf-8",
    )

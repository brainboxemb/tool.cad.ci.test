"""Shared builder used by two synthetic consumer items."""

from pathlib import Path
import os

VERSION = "v1"

builder_name = os.environ["CAD_CI_BUILDER"]
builder_path = Path(os.environ["CAD_CI_BUILDER_PATH"])
item_path = Path(os.environ["CAD_CI_ITEM_PATH"])
output = Path(os.environ["CAD_CI_OUTPUT"])

output.mkdir(parents=True, exist_ok=True)
(output / "result.txt").write_text(
    f"{builder_name}:{builder_path.name}:{item_path.name}:{VERSION}\n",
    encoding="utf-8",
)

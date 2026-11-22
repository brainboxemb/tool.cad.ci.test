from __future__ import annotations

import os
from pathlib import Path
import runpy


REPO = Path(os.environ["CAD_CI_REPO"])
ITEM = Path(os.environ["CAD_CI_ITEM_PATH"])
OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    model = runpy.run_path(str(ITEM / "model.py"))
    name = str(model["MODEL_NAME"])
    contract = (
        ITEM.parent / "verification" / "reference_geometry.json"
    ).read_text(encoding="utf-8")
    shared = (REPO / "shared.txt").read_text(encoding="utf-8")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "result.txt").write_text(
        f"{name}:{shared}{contract}",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

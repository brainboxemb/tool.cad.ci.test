from __future__ import annotations

import os
from pathlib import Path


ITEM = Path(os.environ["CAD_CI_ITEM_PATH"])
OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    root = OUTPUT / "items"
    value = (ITEM / "input.txt").read_text(encoding="utf-8")

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

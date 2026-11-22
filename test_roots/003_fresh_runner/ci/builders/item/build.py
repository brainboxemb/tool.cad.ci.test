from __future__ import annotations

import os
from pathlib import Path


ITEM = Path(os.environ["CAD_CI_ITEM_PATH"])
OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "result.txt").write_text(
        (ITEM / "input.txt").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

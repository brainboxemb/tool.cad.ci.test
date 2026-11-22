from __future__ import annotations

import os
from pathlib import Path


OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "done.txt").write_text("done\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

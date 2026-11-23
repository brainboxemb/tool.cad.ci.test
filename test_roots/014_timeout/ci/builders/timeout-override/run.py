from __future__ import annotations

import os
from pathlib import Path
import time


def main() -> int:
    time.sleep(1.2)
    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "done.txt").write_text("ok\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

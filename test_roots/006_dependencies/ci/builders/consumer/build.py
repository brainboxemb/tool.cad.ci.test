from __future__ import annotations

import os
from pathlib import Path

from cad_ci.context import current_context


ITEM = Path(os.environ["CAD_CI_ITEM_PATH"])


def main() -> int:
    ctx = current_context()
    library = ctx.dependency("library")
    text = library.output("data.txt").read_text(encoding="utf-8")
    text += (ITEM / "input.txt").read_text(encoding="utf-8")
    ctx.output.mkdir(parents=True, exist_ok=True)
    (ctx.output / "result.txt").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

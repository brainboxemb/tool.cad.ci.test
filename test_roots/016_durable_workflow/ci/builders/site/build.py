from __future__ import annotations

import os
from pathlib import Path


OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    site = OUTPUT / "site"
    site.mkdir(parents=True, exist_ok=True)
    (site / "index.html").write_text(
        "<!doctype html><title>durable workflow</title>"
        "<p>synthetic durable site</p>\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

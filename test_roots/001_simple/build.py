from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    source = (ROOT / "hello.md").read_text(encoding="utf-8").rstrip()
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "hello.md").write_text(
        f"{source}\n\nBuilt at: {timestamp}\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

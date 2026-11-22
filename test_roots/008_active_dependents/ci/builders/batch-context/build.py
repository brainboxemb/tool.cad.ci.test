from __future__ import annotations

import json
import os
from pathlib import Path


OUTPUT = Path(os.environ["CAD_CI_OUTPUT"])


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    active = json.loads(os.environ["CAD_CI_ACTIVE_DEPENDENTS_JSON"])
    (OUTPUT / "active.json").write_text(
        json.dumps(active) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

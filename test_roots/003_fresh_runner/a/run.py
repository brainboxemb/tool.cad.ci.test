"""Build item A output from its local input."""

from __future__ import annotations

import os
from pathlib import Path


item = Path(__file__).parent
output = Path(os.environ["CAD_CI_OUTPUT"])
output.mkdir(parents=True, exist_ok=True)
(output / "result.txt").write_text(
    (item / "input.txt").read_text(encoding="utf-8"),
    encoding="utf-8",
)

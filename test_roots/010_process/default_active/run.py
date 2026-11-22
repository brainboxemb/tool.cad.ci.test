"""Write one observable output for process-selection acceptance."""

import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text(Path(__file__).parent.name + "\n", encoding="utf-8")

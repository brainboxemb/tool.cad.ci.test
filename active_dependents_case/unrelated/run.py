import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text("unrelated\n", encoding="utf-8")

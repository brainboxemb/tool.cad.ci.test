import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "prepare.txt").write_text("prepare\n", encoding="utf-8")

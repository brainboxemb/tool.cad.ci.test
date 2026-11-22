import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
(out / "done.txt").write_text("done\n", encoding="utf-8")

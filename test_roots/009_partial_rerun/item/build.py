import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
assert (out / "prepare.txt").is_file()
(out / "build.txt").write_text("build\n", encoding="utf-8")

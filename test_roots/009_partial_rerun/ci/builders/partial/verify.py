import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
assert (out / "build.txt").is_file()
(out / "verify.txt").write_text("verify\n", encoding="utf-8")

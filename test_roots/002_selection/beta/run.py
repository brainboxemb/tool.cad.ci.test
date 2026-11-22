import os
from pathlib import Path

repo = Path(os.environ["CAD_CI_REPO"])
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text(
    (Path(__file__).with_name("input.txt").read_text(encoding="utf-8")
     + (repo / "shared.txt").read_text(encoding="utf-8")),
    encoding="utf-8",
)

import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "data.txt").write_text(
    Path(__file__).with_name("input.txt").read_text(encoding="utf-8"),
    encoding="utf-8",
)

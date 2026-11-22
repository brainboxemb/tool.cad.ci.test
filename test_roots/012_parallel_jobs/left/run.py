import os
from pathlib import Path
import time


time.sleep(1.5)
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text(
    Path(__file__).with_name("input.txt").read_text(encoding="utf-8"),
    encoding="utf-8",
)

"""Build the nested child item independently of its parent output."""

from pathlib import Path
import os

source = Path(__file__).with_name("input.txt").read_text(encoding="utf-8")
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "child.txt").write_text(source, encoding="utf-8")

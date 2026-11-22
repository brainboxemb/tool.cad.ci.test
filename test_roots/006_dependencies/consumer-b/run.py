from pathlib import Path
from cad_ci.context import current_context

ctx = current_context()
lib = ctx.dependency("library")
text = lib.output("data.txt").read_text(encoding="utf-8")
text += Path(__file__).with_name("input.txt").read_text(encoding="utf-8")
ctx.output.mkdir(parents=True, exist_ok=True)
(ctx.output / "result.txt").write_text(text, encoding="utf-8")

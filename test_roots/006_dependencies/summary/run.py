from cad_ci.context import current_context

ctx = current_context()
a = ctx.dependency("consumer-a").output("result.txt").read_text(encoding="utf-8")
b = ctx.dependency("consumer-b").output("result.txt").read_text(encoding="utf-8")
ctx.output.mkdir(parents=True, exist_ok=True)
(ctx.output / "summary.txt").write_text(a + b, encoding="utf-8")

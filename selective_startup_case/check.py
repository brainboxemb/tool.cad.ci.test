#!/usr/bin/env python3
"""Black-box acceptance for selective active-closure preparation."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import run_tool


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repository(repo: Path) -> None:
    shutil.rmtree(repo, ignore_errors=True)
    repo.mkdir(parents=True)

    unrelated = [f"unrelated-{index:02d}" for index in range(40)]
    item_names = ["library", "selected", *unrelated, "symlink-owner"]
    write(
        repo / "cad-ci.yml",
        "schema: 1\nitems: [" + ", ".join(item_names) + "]\n",
    )

    write(repo / "library" / "input.txt", "library-bytes\n")
    write(
        repo / "library" / "run.py",
        """import os
from pathlib import Path
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "lib.txt").write_text(
    Path(__file__).with_name("input.txt").read_text(),
    encoding="utf-8",
)
""",
    )
    write(
        repo / "library" / "ci.yml",
        """id: library
steps:
  - id: build
    inputs: [library/input.txt, library/run.py]
    run: [python, run.py]
    outputs: [lib.txt]
""",
    )

    write(
        repo / "selected" / "run.py",
        """from cad_ci.context import current_context
ctx = current_context()
dependency = ctx.dependency("library")
ctx.output.mkdir(parents=True, exist_ok=True)
(ctx.output / "result.txt").write_text(
    dependency.output("lib.txt").read_text(encoding="utf-8") + "selected\\n",
    encoding="utf-8",
)
""",
    )
    write(
        repo / "selected" / "ci.yml",
        """id: selected
needs: [library]
steps:
  - id: build
    inputs: [selected/run.py]
    run: [python, run.py]
    outputs: [result.txt]
""",
    )

    for name in unrelated:
        write(repo / name / "input.txt", f"{name}\n")
        write(
            repo / name / "ci.yml",
            f"""id: {name}
steps:
  - id: build
    inputs: [{name}/input.txt]
    run: [python, -c, "print('unused')"]
""",
        )

    write(repo / "symlink-owner" / "input.txt", "owned\n")
    write(
        repo / "symlink-owner" / "ci.yml",
        """id: symlink-owner
steps:
  - id: build
    inputs: [symlink-owner/**]
    run: [python, -c, "print('must not run')"]
""",
    )
    link = repo / "symlink-owner" / "matched-link.txt"
    try:
        link.symlink_to(repo / "symlink-owner" / "input.txt")
    except (OSError, NotImplementedError) as exc:
        raise RuntimeError("acceptance runner must support source symlinks") from exc


def main() -> int:
    repo = ROOT / "output" / "cases" / "selective_startup_case"
    make_repository(repo)

    started = time.perf_counter()
    output = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "selected",
    )
    elapsed = time.perf_counter() - started

    assert "symlink" not in output.lower(), output
    assert (repo / "build/library/lib.txt").read_text(encoding="utf-8") == (
        "library-bytes\n"
    )
    assert (repo / "build/selected/result.txt").read_text(encoding="utf-8") == (
        "library-bytes\nselected\n"
    )
    assert (repo / "build/library/.cad-ci/item.json").is_file()
    assert (repo / "build/selected/.cad-ci/item.json").is_file()
    for index in range(40):
        assert not (repo / "build" / f"unrelated-{index:02d}").exists()
    assert not (repo / "build/symlink-owner").exists()

    unsafe = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "symlink-owner",
        expect=2,
    )
    assert "configured source input is a symlink" in unsafe, unsafe
    assert "symlink-owner/matched-link.txt" in unsafe, unsafe

    print(
        "selective_startup_case passed; "
        f"selected released-stack run {elapsed:.3f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

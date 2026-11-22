#!/usr/bin/env python3
"""Black-box Git-selected execution from a fresh cacheless clone."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def git(repo: Path, *args: str) -> str:
    """Run Git in the synthetic acceptance repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def main() -> int:
    """Prove exact base/head selection without any previous SCons state."""

    source = fresh_case(SOURCE, "003_fresh_runner")
    subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
    subprocess.run(
        ["git", "config", "user.name", "tool.cad.ci.test"],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "tool.cad.ci.test@example.invalid"],
        cwd=source,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=source, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "base"],
        cwd=source,
        check=True,
    )
    base = git(source, "rev-parse", "HEAD")

    (source / "a/input.txt").write_text("a-changed\n", encoding="utf-8")
    subprocess.run(["git", "add", "a/input.txt"], cwd=source, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "change a"],
        cwd=source,
        check=True,
    )
    head = git(source, "rev-parse", "HEAD")

    runner = source.parent / "003_fresh_runner_clone"
    shutil.rmtree(runner, ignore_errors=True)
    subprocess.run(
        ["git", "clone", "--quiet", str(source), str(runner)],
        check=True,
    )

    assert git(runner, "rev-parse", "HEAD") == head
    assert not (runner / "build").exists()
    assert not (runner / ".cache/cad-ci").exists()

    plan = run_tool(
        "plan",
        "--repo",
        str(runner),
        "--base",
        base,
        "--head",
        head,
    )
    assert "a\taffected" in plan, plan
    assert "b" not in plan, plan

    run = run_tool(
        "run",
        "--repo",
        str(runner),
        "--base",
        base,
        "--head",
        head,
    )
    assert "built: a:build" in run, run
    assert "b:build" not in run, run

    assert (runner / "build/a/result.txt").read_text(encoding="utf-8") == "a-changed\n"
    assert not (runner / "build/b").exists()

    print("test_roots/003_fresh_runner passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

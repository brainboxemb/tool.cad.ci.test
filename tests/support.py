"""Shared helpers for external black-box acceptance cases.

The reusable workflow already loaded the exact released tool and library stack.
Cases invoke that stack through the public CLI; they do not clone, install or
reimplement it.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import cad_ci_tool


ROOT = Path(__file__).resolve().parents[1]
TOOL_ROOT = Path(cad_ci_tool.__file__).resolve().parents[1]
WORK_ROOT = ROOT / "output" / "cases"


def fresh_case(source: Path, name: str) -> Path:
    """Copy one immutable case template to disposable output/cases/<name>."""

    target = WORK_ROOT / name
    shutil.rmtree(target, ignore_errors=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            "check.py",
            "__pycache__",
            "build",
            ".cache",
        ),
    )
    return target


def run_tool(
    *args: str,
    cwd: Path | None = None,
    expect: int = 0,
) -> str:
    """Run the exact released tool already loaded by the reusable workflow."""

    completed = subprocess.run(
        [sys.executable, "-m", "cad_ci_tool", *args],
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != expect:
        raise AssertionError(
            f"cad-ci exit {completed.returncode}, expected {expect}\n"
            f"command: {' '.join(args)}\n"
            f"{completed.stdout}"
        )
    return completed.stdout


def remove_local_scons_state(repo: Path, *, keep_cache: bool) -> None:
    """Simulate a fresh runner, optionally preserving only SCons CacheDir."""

    shutil.rmtree(repo / "build", ignore_errors=True)
    root = repo / ".cache" / "cad-ci" / "scons"
    if keep_cache:
        shutil.rmtree(root / "state", ignore_errors=True)
        shutil.rmtree(root / "targets", ignore_errors=True)
        shutil.rmtree(root / "run", ignore_errors=True)
    else:
        shutil.rmtree(root, ignore_errors=True)


def read_json(path: Path) -> dict:
    """Read one JSON evidence/manifest file."""

    import json

    return json.loads(path.read_text(encoding="utf-8"))

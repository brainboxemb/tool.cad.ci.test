#!/usr/bin/env python3
"""Black-box acceptance for released bounded parallel SCons jobs."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import run_tool


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repository(repo: Path) -> None:
    shutil.rmtree(repo, ignore_errors=True)
    repo.mkdir(parents=True)

    write(repo / "cad-ci.yml", "schema: 1\nitems: [left, right]\n")

    for name in ("left", "right"):
        write(repo / name / "input.txt", f"{name}\n")
        write(
            repo / name / "run.py",
            """import os
from pathlib import Path
import time

time.sleep(1.5)
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text(
    Path(__file__).with_name("input.txt").read_text(encoding="utf-8"),
    encoding="utf-8",
)
""",
        )
        write(
            repo / name / "ci.yml",
            f"""id: {name}
steps:
  - id: build
    inputs: [{name}/input.txt, {name}/run.py]
    run: [python, run.py]
    outputs: [result.txt]
""",
        )


def parse_timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        raise AssertionError(f"missing action timestamp: {value!r}")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def step_evidence(repo: Path, item: str) -> dict:
    path = repo / "build" / item / ".cad-ci" / "steps" / "build.json"
    if not path.is_file():
        raise AssertionError(f"missing public step evidence: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    repo = ROOT / "output" / "cases" / "parallel_jobs_case"
    make_repository(repo)

    output = run_tool(
        "run",
        "--repo",
        str(repo),
        "--jobs",
        "2",
    )

    left = step_evidence(repo, "left")
    right = step_evidence(repo, "right")

    for name, row in (("left", left), ("right", right)):
        assert row["status"] == "pass", (name, row)
        assert row["outcome"] == "BUILT", (name, row)
        assert row["action_executed"] is True, (name, row)
        result = repo / "build" / name / "result.txt"
        assert result.read_text(encoding="utf-8") == f"{name}\n"

    left_start = parse_timestamp(left["started_at"])
    left_finish = parse_timestamp(left["finished_at"])
    right_start = parse_timestamp(right["started_at"])
    right_finish = parse_timestamp(right["finished_at"])

    assert left_start < left_finish
    assert right_start < right_finish

    # Overlap is the public behavioral proof that the exact released jobs=2
    # stack executed two independent SCons actions concurrently.
    assert left_start < right_finish and right_start < left_finish, (
        left["started_at"],
        left["finished_at"],
        right["started_at"],
        right["finished_at"],
        output,
    )

    print(
        "parallel_jobs_case passed; overlapping action intervals: "
        f"left={left['started_at']}..{left['finished_at']} "
        f"right={right['started_at']}..{right['finished_at']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Black-box acceptance for released bounded parallel jobs."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


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
    repo = fresh_case(SOURCE, "012_parallel_jobs")

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
    assert left_start < right_finish and right_start < left_finish, (
        left["started_at"],
        left["finished_at"],
        right["started_at"],
        right["finished_at"],
        output,
    )

    print(
        "test_roots/012_parallel_jobs passed; overlapping action intervals: "
        f"left={left['started_at']}..{left['finished_at']} "
        f"right={right['started_at']}..{right['finished_at']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

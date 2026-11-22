#!/usr/bin/env python3
"""Black-box acceptance for released dependency-output copy targets."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def step(repo: Path, item: str) -> dict:
    path = repo / "build" / item / ".cad-ci" / "steps" / "materialize.json"
    if not path.is_file():
        raise AssertionError(f"missing copy evidence: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    repo = fresh_case(SOURCE, "dependency_copy_case")

    for name in ("consumer-a", "consumer-b"):
        scripts = list((repo / name).glob("*.py"))
        assert scripts == [], (name, scripts)

    cold = run_tool("run", "--repo", str(repo), "--jobs", "2")
    assert "built: batch:build" in cold
    assert "built: consumer-a:materialize" in cold
    assert "built: consumer-b:materialize" in cold

    for name in ("consumer-a", "consumer-b"):
        evidence = step(repo, name)
        assert evidence["schema"] == 4, evidence
        assert evidence["status"] == "pass", evidence
        assert evidence["outcome"] == "BUILT", evidence
        assert evidence["action_type"] == "copy", evidence
        assert evidence["action_executed"] is True, evidence
        assert evidence["exit_code"] is None, evidence
        assert evidence["timeout_seconds"] is None, evidence
        assert evidence["started_at"], evidence
        assert evidence["finished_at"], evidence
        assert (
            repo / "build" / name / "result.txt"
        ).read_text(encoding="utf-8") == f"{name}:one\n"
        assert (
            repo / "build" / name / "generated" / "value.txt"
        ).read_text(encoding="utf-8") == f"{name}-generated:one\n"

    current = run_tool("run", "--repo", str(repo), "--jobs", "2")
    assert "current: batch:build" in current
    assert "current: consumer-a:materialize" in current
    assert "current: consumer-b:materialize" in current

    for name in ("consumer-a", "consumer-b"):
        evidence = step(repo, name)
        assert evidence["schema"] == 4, evidence
        assert evidence["outcome"] == "CURRENT", evidence
        assert evidence["action_type"] == "copy", evidence
        assert evidence["action_executed"] is False, evidence
        assert evidence["started_at"] is None, evidence
        assert evidence["finished_at"] is None, evidence

    print("dependency_copy_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

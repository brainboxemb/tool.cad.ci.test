#!/usr/bin/env python3
"""Black-box acceptance for active direct-dependent command context."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def active(repo: Path) -> list[str]:
    return json.loads(
        (repo / "build" / "batch" / "active.json").read_text(encoding="utf-8")
    )


def evidence(repo: Path) -> dict:
    path = repo / "build" / "batch" / ".cad-ci" / "steps" / "build.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    repo = fresh_case(SOURCE, "008_active_dependents")

    only_a = run_tool(
        "run", "--repo", str(repo), "--item", "consumer-a",
    )
    assert "built: batch:build" in only_a
    assert "built: consumer-a:verify" in only_a
    assert "consumer-b:verify" not in only_a
    assert active(repo) == ["consumer-a"]
    first = evidence(repo)
    assert first["schema"] == 5
    assert first["active_dependents"] == ["consumer-a"]

    same_a = run_tool(
        "run", "--repo", str(repo), "--item", "consumer-a",
    )
    assert "current: batch:build" in same_a
    assert active(repo) == ["consumer-a"]
    assert evidence(repo)["active_dependents"] == ["consumer-a"]

    only_b = run_tool(
        "run", "--repo", str(repo), "--item", "consumer-b",
    )
    assert "built: batch:build" in only_b
    assert "built: consumer-b:verify" in only_b
    assert "consumer-a:verify" not in only_b
    assert active(repo) == ["consumer-b"]
    second = evidence(repo)
    assert second["active_dependents"] == ["consumer-b"]
    assert second["target_spec_digest"] != first["target_spec_digest"]

    (repo / "batch" / "input.txt").write_text("two\n", encoding="utf-8")
    both = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "batch/input.txt",
        "--jobs",
        "2",
    )
    assert both.count("CAD CI run: batch:build") == 1, both
    assert "built: consumer-a:verify" in both
    assert "built: consumer-b:verify" in both
    assert active(repo) == ["consumer-a", "consumer-b"]
    both_evidence = evidence(repo)
    assert both_evidence["schema"] == 5
    assert both_evidence["active_dependents"] == ["consumer-a", "consumer-b"]

    full = run_tool("run", "--repo", str(repo), "--jobs", "2")
    assert active(repo) == ["consumer-a", "consumer-b"]
    assert "unrelated:verify" in full
    assert evidence(repo)["active_dependents"] == ["consumer-a", "consumer-b"]

    print("test_roots/008_active_dependents passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

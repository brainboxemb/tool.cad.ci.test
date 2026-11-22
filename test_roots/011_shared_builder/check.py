#!/usr/bin/env python3
"""Black-box acceptance for declarative shared-builder configuration."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def main() -> int:
    for item in ("a", "b"):
        text = (SOURCE / "items" / item / "ci.yml").read_text(encoding="utf-8")
        assert "builder: shared" in text
        assert "steps:" not in text
        assert "run:" not in text

    repo = fresh_case(SOURCE, "011_shared_builder")

    first = run_tool("run", "--repo", str(repo))
    assert "built: a:build" in first
    assert "built: b:build" in first
    assert (repo / "build" / "items" / "a" / "result.txt").read_text(
        encoding="utf-8"
    ) == "shared:shared:a:v1\n"
    assert (repo / "build" / "items" / "b" / "result.txt").read_text(
        encoding="utf-8"
    ) == "shared:shared:b:v1\n"

    second = run_tool("run", "--repo", str(repo))
    assert "current: a:build" in second
    assert "current: b:build" in second

    changed = "ci/builders/shared/build.py"
    plan = run_tool(
        "plan",
        "--repo",
        str(repo),
        "--changed",
        changed,
    )
    assert "a\taffected" in plan
    assert "b\taffected" in plan

    builder = repo / changed
    builder.write_text(
        builder.read_text(encoding="utf-8").replace(
            'VERSION = "v1"',
            'VERSION = "v2"',
        ),
        encoding="utf-8",
    )
    rebuilt = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        changed,
    )
    assert "built: a:build" in rebuilt
    assert "built: b:build" in rebuilt
    assert (repo / "build" / "items" / "a" / "result.txt").read_text(
        encoding="utf-8"
    ) == "shared:shared:a:v2\n"
    assert (repo / "build" / "items" / "b" / "result.txt").read_text(
        encoding="utf-8"
    ) == "shared:shared:b:v2\n"

    print("test_roots/011_shared_builder passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

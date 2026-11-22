#!/usr/bin/env python3
"""Black-box changed-item selection acceptance."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "002_selection")

    cold = run_tool("run", "--repo", str(repo))
    assert "built: alpha:build" in cold
    assert "built: beta:build" in cold

    plan_alpha = run_tool(
        "plan",
        "--repo",
        str(repo),
        "--changed",
        "alpha/input.txt",
    )
    assert "alpha\taffected" in plan_alpha
    assert "beta" not in plan_alpha

    (repo / "alpha/input.txt").write_text("alpha-two\n", encoding="utf-8")
    alpha_only = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "alpha/input.txt",
    )
    assert "built: alpha:build" in alpha_only
    assert "beta:build" not in alpha_only

    plan_shared = run_tool(
        "plan",
        "--repo",
        str(repo),
        "--changed",
        "shared.txt",
    )
    assert "alpha\taffected" in plan_shared
    assert "beta\taffected" in plan_shared

    (repo / "shared.txt").write_text("shared-two\n", encoding="utf-8")
    shared = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "shared.txt",
    )
    assert "built: alpha:build" in shared
    assert "built: beta:build" in shared

    print("test_roots/002_selection passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

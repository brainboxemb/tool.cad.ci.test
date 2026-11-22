#!/usr/bin/env python3
"""Black-box exact step, until and from acceptance."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def item_evidence(repo: Path) -> Path:
    return repo / "build/item/.cad-ci/item.json"


def main() -> int:
    repo = fresh_case(SOURCE, "009_partial_rerun")

    cold = run_tool("run", "--repo", str(repo))
    assert "built: partial-case:prepare" in cold
    assert "built: partial-case:build" in cold
    assert "built: partial-case:verify" in cold
    assert item_evidence(repo).is_file()

    exact = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "partial-case",
        "--step",
        "build",
    )
    assert "current: partial-case:prepare" in exact
    assert "built: partial-case:build" in exact
    assert "partial-case:verify" not in exact
    assert not item_evidence(repo).exists()

    run_tool("run", "--repo", str(repo))
    assert item_evidence(repo).is_file()

    until = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "partial-case",
        "--until",
        "build",
    )
    assert "current: partial-case:prepare" in until
    assert "current: partial-case:build" in until
    assert "partial-case:verify" not in until
    assert not item_evidence(repo).exists()

    run_tool("run", "--repo", str(repo))
    from_build = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "partial-case",
        "--from",
        "build",
    )
    assert "current: partial-case:prepare" in from_build
    assert "built: partial-case:build" in from_build
    assert "built: partial-case:verify" in from_build
    assert item_evidence(repo).is_file()

    print("test_roots/009_partial_rerun passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

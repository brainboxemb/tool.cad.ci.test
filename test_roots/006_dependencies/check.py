#!/usr/bin/env python3
"""Black-box dependency fan-out and direct-summary acceptance."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "006_dependencies")

    cold = run_tool("run", "--repo", str(repo))
    for key in (
        "library:prepare",
        "library:finish",
        "consumer-a:build",
        "consumer-b:build",
        "summary:build",
    ):
        assert f"built: {key}" in cold

    current = run_tool("run", "--repo", str(repo))
    assert "current: summary:build" in current

    (repo / "consumer-a/input.txt").write_text("a-two\n", encoding="utf-8")
    one_consumer = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "consumer-a/input.txt",
    )
    assert "built: consumer-a:build" in one_consumer
    assert "consumer-b:build" not in one_consumer
    assert "summary:build" not in one_consumer

    (repo / "library/input.txt").write_text("library-two\n", encoding="utf-8")
    library_change = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "library/input.txt",
    )
    assert "built: library:prepare" in library_change
    assert "built: library:finish" in library_change
    assert "built: consumer-a:build" in library_change
    assert "built: consumer-b:build" in library_change
    assert "summary:build" not in library_change

    explicit_summary = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "summary",
    )
    assert "built: summary:build" in explicit_summary
    assert "current: consumer-a:build" in explicit_summary
    assert "current: consumer-b:build" in explicit_summary

    print("test_roots/006_dependencies passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

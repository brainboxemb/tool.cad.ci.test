#!/usr/bin/env python3
"""Black-box acceptance for the smallest standalone test repository."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def timestamp(text: str) -> str:
    """Return the timestamp written by the dummy build."""

    marker = "Built at: "
    lines = [line for line in text.splitlines() if line.startswith(marker)]
    if len(lines) != 1:
        raise AssertionError(f"expected one build timestamp, got: {lines!r}")
    return lines[0][len(marker):]


def main() -> int:
    repo = fresh_case(SOURCE, "001_simple")
    output = repo / "build" / "hello.md"

    first = run_tool("run", "--repo", str(repo))
    assert "built: test-case-1-simple:build" in first
    first_text = output.read_text(encoding="utf-8")
    assert first_text.startswith("Hello\n\nBuilt at: ")
    first_timestamp = timestamp(first_text)

    second = run_tool("run", "--repo", str(repo))
    assert "current: test-case-1-simple:build" in second
    assert output.read_text(encoding="utf-8") == first_text

    (repo / "hello.md").write_text("Hello again\n", encoding="utf-8")
    third = run_tool("run", "--repo", str(repo))
    assert "built: test-case-1-simple:build" in third
    third_text = output.read_text(encoding="utf-8")
    assert third_text.startswith("Hello again\n\nBuilt at: ")
    assert timestamp(third_text) != first_timestamp

    print("test_roots/001_simple passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

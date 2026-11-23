#!/usr/bin/env python3
"""Black-box released CadQuery Assembly export acceptance."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def require_stl(repo: Path) -> None:
    """Require the public projected Assembly STL to exist and be non-empty."""

    stl = repo / "build" / "models" / "assembly" / "model.stl"
    assert stl.is_file(), stl
    assert stl.stat().st_size > 0, stl


def main() -> int:
    """Prove released CadQuery Assembly export and identical-run reuse."""

    repo = fresh_case(SOURCE, "019_cadquery_assembly")

    first = run_tool("run", "--repo", str(repo))
    assert first.count("CAD CI built-in batch:") == 1, first
    assert "cadquery-assembly=pass" in first, first
    assert "built: cad-ci-runtime-reference:build" in first, first
    require_stl(repo)

    second = run_tool("run", "--repo", str(repo))
    assert "CAD CI built-in batch:" not in second, second
    assert "current: cad-ci-runtime-reference:build" in second, second
    require_stl(repo)

    print("test_roots/019_cadquery_assembly passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

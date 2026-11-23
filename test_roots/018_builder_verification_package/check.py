#!/usr/bin/env python3
"""Black-box repository-builder verification-package acceptance."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent


def main() -> int:
    """Prove public wheel injection, CURRENT reuse and wildcard selection."""

    item_text = (SOURCE / "models" / "a" / "ci.yml").read_text(
        encoding="utf-8"
    )
    builder_text = (
        SOURCE / "ci" / "builders" / "wheel-consumer" / "builder.yml"
    ).read_text(encoding="utf-8")
    assert "builder: wheel-consumer" in item_text
    assert "needs:" not in item_text
    assert "verification_package: true" in builder_text

    repo = fresh_case(SOURCE, "018_builder_verification_package")

    plan = run_tool(
        "plan",
        "--repo",
        str(repo),
        "--changed",
        "models/a/scpf/model.py",
    )
    assert "wheel-consumer\taffected" in plan, plan

    first = run_tool("run", "--repo", str(repo))
    assert "built: wheel-consumer:inspect" in first, first
    result_path = repo / "build" / "models" / "a" / "wheel.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["schema"] == 1, result
    assert result["version"] == "0.16.0", result
    assert result["wheel"].endswith(".whl"), result

    second = run_tool("run", "--repo", str(repo))
    assert "current: wheel-consumer:inspect" in second, second
    assert json.loads(result_path.read_text(encoding="utf-8")) == result

    print("test_roots/018_builder_verification_package passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

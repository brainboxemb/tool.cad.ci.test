#!/usr/bin/env python3
"""Black-box released built-in builder + verification acceptance."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool


SOURCE = Path(__file__).resolve().parent
ITEMS = ("build123d", "cadquery")


def verification_report(repo: Path, name: str) -> dict:
    """Read one public projected verification report."""

    path = (
        repo
        / "build"
        / "models"
        / name
        / "verification"
        / "verification.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def require_outputs(repo: Path) -> None:
    """Require both public STL and verification outputs to pass."""

    for name in ITEMS:
        stl = repo / "build" / "models" / name / "model.stl"
        assert stl.is_file() and stl.stat().st_size > 0, stl
        report = verification_report(repo, name)
        assert report["status"] == "pass", report
        checks = report.get("checks", [])
        assert len(checks) == 1, checks
        assert checks[0]["id"] == "geometry", checks
        assert checks[0]["status"] == "pass", checks


def main() -> int:
    """Prove shared released runtime build, verification and CURRENT reuse."""

    repo = fresh_case(SOURCE, "017_builtin_verification")

    first = run_tool("run", "--repo", str(repo))
    assert first.count("CAD CI built-in batch:") == 1, first
    assert "reference-build123d=pass" in first, first
    assert "reference-cadquery=pass" in first, first
    assert "built: cad-ci-runtime-reference:build" in first, first
    assert "built: reference-build123d:verify" in first, first
    assert "built: reference-cadquery:verify" in first, first
    require_outputs(repo)

    second = run_tool("run", "--repo", str(repo))
    assert "CAD CI built-in batch:" not in second, second
    assert "current: cad-ci-runtime-reference:build" in second, second
    assert "current: reference-build123d:verify" in second, second
    assert "current: reference-cadquery:verify" in second, second
    require_outputs(repo)

    shared = repo / "verification" / "reference_geometry.json"
    data = json.loads(shared.read_text(encoding="utf-8"))
    data["bounds_tolerance_mm"] = 0.10
    shared.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    plan = run_tool(
        "plan",
        "--repo",
        str(repo),
        "--changed",
        "verification/reference_geometry.json",
    )
    assert "reference-build123d\taffected" in plan, plan
    assert "reference-cadquery\taffected" in plan, plan

    try:
        changed = run_tool(
            "run",
            "--repo",
            str(repo),
            "--changed",
            "verification/reference_geometry.json",
        )
    except AssertionError as exc:
        evidence_path = (
            repo
            / "build"
            / ".cad-ci-runtime"
            / "reference"
            / ".cad-ci"
            / "steps"
            / "build.json"
        )
        evidence = (
            json.loads(evidence_path.read_text(encoding="utf-8"))
            if evidence_path.is_file()
            else {"missing": str(evidence_path)}
        )
        raise AssertionError(
            f"{exc}\nshared runtime action evidence:\n"
            f"{json.dumps(evidence, indent=2, sort_keys=True)}"
        ) from exc
    assert changed.count("CAD CI built-in batch:") == 1, changed
    assert "reference-build123d=pass" in changed, changed
    assert "reference-cadquery=pass" in changed, changed
    require_outputs(repo)

    print("test_roots/017_builtin_verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

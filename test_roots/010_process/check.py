#!/usr/bin/env python3
"""Black-box item process participation acceptance."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "010_process")

    plan = json.loads(run_tool("plan", "--repo", str(repo), "--json"))
    ids = [row["id"] for row in plan]
    assert ids == ["default-active", "explicit-active"], plan
    assert "disabled" not in ids

    run = run_tool("run", "--repo", str(repo))
    assert "built: default-active:build" in run
    assert "built: explicit-active:build" in run
    assert "disabled:build" not in run

    assert (repo / "build/default_active/result.txt").is_file()
    assert (repo / "build/explicit_active/result.txt").is_file()
    assert (repo / "build/default_active/.cad-ci/item.json").is_file()
    assert (repo / "build/explicit_active/.cad-ci/item.json").is_file()
    assert not (repo / "build/disabled").exists()

    prepared = repo / "prepared-main"
    run_tool(
        "build",
        "prepare-main",
        "--repo",
        str(repo),
        "--candidate-root",
        str(repo / "build"),
        "--out",
        str(prepared),
        "--source-commit",
        "process-case-main",
    )
    assert (prepared / "default_active/.cad-ci/item.json").is_file()
    assert (prepared / "explicit_active/.cad-ci/item.json").is_file()
    assert not (prepared / "disabled").exists()
    manifest = json.loads((prepared / "build.json").read_text(encoding="utf-8"))
    assert set(manifest["items"]) == {
        "default_active",
        "explicit_active",
    }, manifest

    explicit = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "disabled",
        expect=2,
    )
    assert "item is not processed: disabled" in explicit

    print("test_roots/010_process passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

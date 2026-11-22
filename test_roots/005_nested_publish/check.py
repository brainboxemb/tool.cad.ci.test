#!/usr/bin/env python3
"""Black-box durable ownership acceptance for nested parent/child items."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, read_json, run_tool

SOURCE = Path(__file__).resolve().parent


def item_state(root: Path, relative: str) -> bytes:
    """Return exact complete-item evidence bytes for preservation checks."""

    return (root / relative / ".cad-ci" / "item.json").read_bytes()


def main() -> int:
    repo = fresh_case(SOURCE, "005_nested_publish")

    cold = run_tool("run", "--repo", str(repo))
    assert "built: parent:build" in cold, cold
    assert "built: child:build" in cold, cold

    candidate = repo / "build"
    out = ROOT / "output" / "005_nested_publish"
    out.mkdir(parents=True, exist_ok=True)

    main_scope = out / "main"
    run_tool(
        "build",
        "prepare-main",
        "--repo",
        str(repo),
        "--candidate-root",
        str(candidate),
        "--out",
        str(main_scope),
        "--source-commit",
        "main-v1",
    )

    manifest = read_json(main_scope / "build.json")
    assert manifest["items"]["items/model"]["outputs"] == ["result.txt"], manifest
    assert manifest["items"]["items/model/reference"]["outputs"] == ["result.txt"], manifest
    assert (main_scope / "items/model/result.txt").read_text() == "parent-v1\n"
    assert (main_scope / "items/model/reference/result.txt").read_text() == "child-v1\n"

    both_overlay = out / "both-overlay"
    run_tool(
        "build",
        "prepare-pr",
        "--repo",
        str(repo),
        "--candidate-root",
        str(candidate),
        "--out",
        str(both_overlay),
        "--source-commit",
        "pr-both",
        "--pull-request",
        "7",
        "--items",
        "parent",
        "child",
    )
    both_manifest = read_json(both_overlay / "build.json")
    assert set(both_manifest["items"]) == {
        "items/model",
        "items/model/reference",
    }, both_manifest
    assert (both_overlay / "items/model/result.txt").is_file()
    assert (both_overlay / "items/model/reference/result.txt").is_file()

    child_overlay = out / "child-overlay"
    run_tool(
        "build",
        "prepare-pr",
        "--repo",
        str(repo),
        "--candidate-root",
        str(candidate),
        "--out",
        str(child_overlay),
        "--source-commit",
        "pr-child",
        "--pull-request",
        "8",
        "--items",
        "child",
    )
    assert not (child_overlay / "items/model/result.txt").exists()
    assert not (child_overlay / "items/model/.cad-ci").exists()
    assert (child_overlay / "items/model/reference/result.txt").is_file()
    assert (child_overlay / "items/model/reference/.cad-ci/item.json").is_file()

    child_before = (
        main_scope / "items/model/reference/result.txt"
    ).read_bytes()
    child_state_before = item_state(main_scope, "items/model/reference")

    parent_input = repo / "items/model/input.txt"
    parent_input.write_text("parent-v2\n", encoding="utf-8")
    parent_run = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "items/model/input.txt",
    )
    assert "built: parent:build" in parent_run, parent_run
    assert "child:build" not in parent_run, parent_run

    parent_updated = out / "parent-updated"
    run_tool(
        "build",
        "update-main",
        "--repo",
        str(repo),
        "--candidate-root",
        str(candidate),
        "--main",
        str(main_scope),
        "--out",
        str(parent_updated),
        "--source-commit",
        "main-parent-v2",
        "--items",
        "parent",
    )
    assert (parent_updated / "items/model/result.txt").read_text() == "parent-v2\n"
    assert (
        parent_updated / "items/model/reference/result.txt"
    ).read_bytes() == child_before
    assert item_state(
        parent_updated,
        "items/model/reference",
    ) == child_state_before

    parent_before = (
        parent_updated / "items/model/result.txt"
    ).read_bytes()
    parent_state_before = item_state(parent_updated, "items/model")

    child_input = repo / "items/model/reference/input.txt"
    child_input.write_text("child-v2\n", encoding="utf-8")
    child_run = run_tool(
        "run",
        "--repo",
        str(repo),
        "--changed",
        "items/model/reference/input.txt",
    )
    assert "built: child:build" in child_run, child_run
    assert "parent:build" not in child_run, child_run

    child_updated = out / "child-updated"
    run_tool(
        "build",
        "update-main",
        "--repo",
        str(repo),
        "--candidate-root",
        str(candidate),
        "--main",
        str(parent_updated),
        "--out",
        str(child_updated),
        "--source-commit",
        "main-child-v2",
        "--items",
        "child",
    )
    assert (
        child_updated / "items/model/result.txt"
    ).read_bytes() == parent_before
    assert item_state(child_updated, "items/model") == parent_state_before
    assert (
        child_updated / "items/model/reference/result.txt"
    ).read_text() == "child-v2\n"

    print("test_roots/005_nested_publish passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

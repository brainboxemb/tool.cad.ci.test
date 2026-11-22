#!/usr/bin/env python3
"""Black-box nested item paths, templates and Git selection acceptance."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def git(repo: Path, *args: str) -> str:
    """Run Git in one synthetic consumer repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def fresh_clone(source: Path, target: Path) -> Path:
    """Clone source and prove no generated CAD-CI state came with it."""

    shutil.rmtree(target, ignore_errors=True)
    subprocess.run(
        ["git", "clone", "--quiet", str(source), str(target)],
        check=True,
    )
    assert not (target / "build").exists()
    assert not (target / ".cache/cad-ci").exists()
    return target


def main() -> int:
    """Prove child-local and parent-shared nested selection from outside."""

    source = fresh_case(SOURCE, "004_nested_items")
    subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
    subprocess.run(
        ["git", "config", "user.name", "tool.cad.ci.test"],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "tool.cad.ci.test@example.invalid"],
        cwd=source,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=source, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "base"],
        cwd=source,
        check=True,
    )
    base = git(source, "rev-parse", "HEAD")

    # First prove a child-local source change selects only that child.
    build123d = source / "examples/attach-angle/build123d/model.py"
    build123d.write_text(
        build123d.read_text(encoding="utf-8") + "\n# changed\n",
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", "examples/attach-angle/build123d/model.py"],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "change build123d"],
        cwd=source,
        check=True,
    )
    child_head = git(source, "rev-parse", "HEAD")

    child_runner = fresh_clone(
        source,
        source.parent / "004_nested_items_child_clone",
    )
    assert git(child_runner, "rev-parse", "HEAD") == child_head

    child_plan = json.loads(
        run_tool(
            "plan",
            "--repo",
            str(child_runner),
            "--base",
            base,
            "--head",
            child_head,
            "--json",
        )
    )
    assert child_plan == [
        {
            "id": "examples-attach-angle-build123d",
            "path": "examples/attach-angle/build123d",
            "kind": "reference",
            "reason": "affected",
        }
    ], child_plan

    child_run = run_tool(
        "run",
        "--repo",
        str(child_runner),
        "--base",
        base,
        "--head",
        child_head,
    )
    assert "built: examples-attach-angle-build123d:build" in child_run, child_run
    assert "examples-attach-angle-cadquery" not in child_run, child_run

    child_result = (
        child_runner
        / "build"
        / "examples"
        / "attach-angle"
        / "build123d"
        / "result.txt"
    )
    assert child_result.read_text(encoding="utf-8") == (
        "build123d:shared\ncontract-v1\n"
    )
    assert not (
        child_runner
        / "build"
        / "examples"
        / "attach-angle"
        / "cadquery"
    ).exists()

    # Then prove the shared parent contract selects both child references.
    contract = (
        source
        / "examples"
        / "attach-angle"
        / "verification"
        / "reference_geometry.json"
    )
    contract.write_text("contract-v2\n", encoding="utf-8")
    subprocess.run(
        [
            "git",
            "add",
            "examples/attach-angle/verification/reference_geometry.json",
        ],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "change parent contract"],
        cwd=source,
        check=True,
    )
    contract_head = git(source, "rev-parse", "HEAD")

    contract_runner = fresh_clone(
        source,
        source.parent / "004_nested_items_contract_clone",
    )
    assert git(contract_runner, "rev-parse", "HEAD") == contract_head

    contract_plan = json.loads(
        run_tool(
            "plan",
            "--repo",
            str(contract_runner),
            "--base",
            child_head,
            "--head",
            contract_head,
            "--json",
        )
    )
    by_id = {row["id"]: row for row in contract_plan}
    assert set(by_id) == {
        "examples-attach-angle-build123d",
        "examples-attach-angle-cadquery",
    }, contract_plan
    assert all(row["reason"] == "affected" for row in by_id.values())

    contract_run = run_tool(
        "run",
        "--repo",
        str(contract_runner),
        "--base",
        child_head,
        "--head",
        contract_head,
    )
    for item_id in (
        "examples-attach-angle-build123d",
        "examples-attach-angle-cadquery",
    ):
        assert f"built: {item_id}:build" in contract_run, contract_run

    for name in ("build123d", "cadquery"):
        result = (
            contract_runner
            / "build"
            / "examples"
            / "attach-angle"
            / name
            / "result.txt"
        )
        assert result.read_text(encoding="utf-8") == (
            f"{name}:shared\ncontract-v2\n"
        )

    print("test_roots/004_nested_items passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

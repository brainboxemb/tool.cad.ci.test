#!/usr/bin/env python3
"""Black-box timeout, override and command-failure acceptance."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, read_json, run_tool


SOURCE = Path(__file__).resolve().parent


def step_evidence(repo: Path, folder: str) -> dict:
    return read_json(repo / f"build/{folder}/.cad-ci/steps/run.json")


def main() -> int:
    repo = fresh_case(SOURCE, "014_timeout")

    timed_out = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "timeout-default",
        expect=2,
    )
    assert "ERROR:" in timed_out
    timeout_state = step_evidence(repo, "wait")
    assert timeout_state["status"] == "timeout"
    assert timeout_state["outcome"] == "ERROR"
    assert timeout_state["timeout_seconds"] == 1
    assert timeout_state["exit_code"] is None
    assert timeout_state["schema"] == 6
    assert timeout_state["action_type"] == "command"
    assert timeout_state["action_executed"] is True
    assert timeout_state["started_at"]
    assert timeout_state["finished_at"]
    assert timeout_state["run_started_at"]
    assert timeout_state["run_finished_at"]
    assert not (repo / "build/wait/.cad-ci/item.json").exists()

    override = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "timeout-override",
    )
    assert "built: timeout-override:run" in override
    override_state = step_evidence(repo, "override")
    assert override_state["status"] == "pass"
    assert override_state["timeout_seconds"] == 3
    assert override_state["schema"] == 6
    assert override_state["action_type"] == "command"
    assert override_state["action_executed"] is True
    assert override_state["started_at"]
    assert override_state["finished_at"]
    assert (repo / "build/override/.cad-ci/item.json").is_file()

    failed = run_tool(
        "run",
        "--repo",
        str(repo),
        "--item",
        "command-failure",
        expect=2,
    )
    assert "ERROR:" in failed
    failure_state = step_evidence(repo, "fail")
    assert failure_state["status"] == "fail"
    assert failure_state["outcome"] == "ERROR"
    assert failure_state["exit_code"] == 3
    assert failure_state["schema"] == 6
    assert failure_state["action_type"] == "command"
    assert failure_state["action_executed"] is True
    assert failure_state["started_at"]
    assert failure_state["finished_at"]
    assert not (repo / "build/fail/.cad-ci/item.json").exists()

    print("test_roots/014_timeout passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

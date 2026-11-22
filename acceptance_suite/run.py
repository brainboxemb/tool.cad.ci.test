#!/usr/bin/env python3
"""Run the external released-stack acceptance cases in one configured CI step."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import traceback


ROOT = Path(__file__).resolve().parents[1]

CASES = (
    "workflow_case/check.py",
    "simple_case1/check.py",
    "more_complex_case2/check.py",
    "logging_case/check.py",
    "fresh_runner_case/check.py",
    "nested_item_case/check.py",
    "nested_publish_case/check.py",
    "dependency_case/check.py",
    "dependency_copy_case/check.py",
    "active_dependents_case/check.py",
    "partial_rerun_case/check.py",
    "process_case/check.py",
    "selective_startup_case/check.py",
    "parallel_jobs_case/check.py",
    "directory_output_case/check.py",
    "timeout_case/check.py",
    "publish_case/check.py",
    "merge_policy_case/check.py",
    "merge_policy_case/check_command.py",
)


def run_case(relative: str, index: int) -> None:
    """Load one acceptance script and call its public main function."""

    path = ROOT / relative
    module_name = f"_acceptance_case_{index}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load acceptance case: {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    main = getattr(module, "main", None)
    if main is None:
        raise RuntimeError(f"acceptance case has no main(): {relative}")

    print(f"\n=== {relative} ===", flush=True)
    result = main()
    if result not in (None, 0):
        raise RuntimeError(f"{relative}: main() returned {result!r}")


def main() -> int:
    """Run every black-box case against the already loaded released tool stack."""

    failures: list[str] = []
    for index, relative in enumerate(CASES):
        try:
            run_case(relative, index)
        except BaseException as exc:
            failures.append(f"{relative}: {exc}")
            traceback.print_exc()

    if failures:
        raise RuntimeError(
            "released-stack acceptance failed:\n- " + "\n- ".join(failures)
        )

    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "accepted.txt").write_text(
        "tool.cad.ci v0.23.0 released-stack acceptance passed\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

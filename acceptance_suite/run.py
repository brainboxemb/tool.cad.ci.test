#!/usr/bin/env python3
"""Run the external released-stack acceptance cases in one configured CI step."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[1]

from contracts import validate_test_roots


SOFT_TOTAL_BUDGET_SECONDS = 30.0
DEFAULT_SOFT_CASE_BUDGET_SECONDS = 3.0
SOFT_CASE_BUDGET_SECONDS = {
    "test_roots/014_timeout/check.py": 4.0,
    "test_roots/015_publish/check.py": 7.0,
}


CASES = (
    "workflow_case/check.py",
    "test_roots/001_simple/check.py",
    "test_roots/002_selection/check.py",
    "test_roots/003_fresh_runner/check.py",
    "test_roots/004_nested_items/check.py",
    "test_roots/005_nested_publish/check.py",
    "test_roots/006_dependencies/check.py",
    "test_roots/007_dependency_copy/check.py",
    "test_roots/008_active_dependents/check.py",
    "test_roots/009_partial_rerun/check.py",
    "test_roots/010_process/check.py",
    "test_roots/011_shared_builder/check.py",
    "test_roots/012_parallel_jobs/check.py",
    "test_roots/013_directory_output/check.py",
    "test_roots/014_timeout/check.py",
    "test_roots/015_publish/check.py",
    "merge_policy_case/check.py",
    "merge_policy_case/check_command.py",
)


def require_case_documentation(relative: str) -> None:
    """Require one local status-bearing README for every registered case."""

    case_root = (ROOT / relative).parent
    readme = case_root / "README.md"
    if not readme.is_file():
        raise RuntimeError(f"registered acceptance case has no README: {case_root.name}")
    text = readme.read_text(encoding="utf-8")
    status = next(
        (line for line in text.splitlines() if line.startswith("Status:")),
        "",
    )
    if not status:
        raise RuntimeError(f"acceptance case README has no Status: {readme}")
    if "obsolete" in status.lower():
        raise RuntimeError(
            f"obsolete acceptance case is still registered: {case_root.name}"
        )


def run_case(relative: str, index: int) -> None:
    """Load one documented acceptance script and call its public main function."""

    require_case_documentation(relative)
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
    """Run every black-box case and record centrally managed timing evidence."""

    validate_test_roots(ROOT)

    failures: list[str] = []
    timings: list[dict[str, object]] = []

    for index, relative in enumerate(CASES):
        started = time.perf_counter()
        outcome = "pass"
        try:
            run_case(relative, index)
        except BaseException as exc:
            outcome = "fail"
            failures.append(f"{relative}: {exc}")
            traceback.print_exc()
        finally:
            elapsed = time.perf_counter() - started
            timings.append(
                {
                    "case": relative,
                    "outcome": outcome,
                    "seconds": round(elapsed, 6),
                }
            )
            print(
                f"duration: {elapsed:.3f}s [{outcome}] {relative}",
                flush=True,
            )

    total_seconds = sum(float(row["seconds"]) for row in timings)
    slowest = sorted(
        timings,
        key=lambda row: float(row["seconds"]),
        reverse=True,
    )

    print("\n=== acceptance timing: slowest first ===", flush=True)
    for row in slowest:
        print(
            f"{float(row['seconds']):8.3f}s "
            f"[{row['outcome']}] {row['case']}",
            flush=True,
        )
    print(
        f"TOTAL {total_seconds:.3f}s across {len(timings)} cases",
        flush=True,
    )

    budget_warnings: list[str] = []
    for row in timings:
        case = str(row["case"])
        seconds = float(row["seconds"])
        budget = SOFT_CASE_BUDGET_SECONDS.get(
            case,
            DEFAULT_SOFT_CASE_BUDGET_SECONDS,
        )
        exceeded = seconds > budget
        row["soft_budget_seconds"] = budget
        row["soft_budget_exceeded"] = exceeded
        if exceeded:
            budget_warnings.append(
                f"{case}: {seconds:.3f}s > {budget:.3f}s"
            )

    total_budget_exceeded = total_seconds > SOFT_TOTAL_BUDGET_SECONDS
    print("\n=== acceptance soft timing budgets ===", flush=True)
    if total_budget_exceeded:
        print(
            "SOFT BUDGET WARNING: "
            f"total {total_seconds:.3f}s > "
            f"{SOFT_TOTAL_BUDGET_SECONDS:.3f}s",
            flush=True,
        )
    for warning in budget_warnings:
        print(f"SOFT BUDGET WARNING: {warning}", flush=True)
    if not total_budget_exceeded and not budget_warnings:
        print(
            "Soft timing budgets satisfied; warnings remain non-failing.",
            flush=True,
        )

    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "case-durations.json").write_text(
        json.dumps(
            {
                "schema": 2,
                "total_case_seconds": round(total_seconds, 6),
                "soft_total_budget_seconds": SOFT_TOTAL_BUDGET_SECONDS,
                "soft_total_budget_exceeded": total_budget_exceeded,
                "default_soft_case_budget_seconds": (
                    DEFAULT_SOFT_CASE_BUDGET_SECONDS
                ),
                "soft_case_budget_overrides_seconds": (
                    SOFT_CASE_BUDGET_SECONDS
                ),
                "soft_budget_warning_count": (
                    len(budget_warnings)
                    + int(total_budget_exceeded)
                ),
                "cases": timings,
                "slowest_first": [str(row["case"]) for row in slowest],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    if failures:
        raise RuntimeError(
            "released-stack acceptance failed:\n- " + "\n- ".join(failures)
        )

    (output / "accepted.txt").write_text(
        "tool.cad.ci v0.29.0 released-stack acceptance passed\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

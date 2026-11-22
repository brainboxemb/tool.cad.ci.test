# Acceptance suite

Status: current

## Purpose

This is the single configured entrypoint for external released-stack
acceptance. Root `cad-ci.yml` selects this item and `run.py` executes the
registered black-box cases against the already loaded released tool/library
stack.

## Registration contract

`run.py::CASES` is the authoritative case list.

Every registered check belongs to one documented case root. Numbered synthetic
consumer repositories live below `test_roots/NNN_name/`; their `check.py` sits
in that repository root. Each case root must have a local `README.md` that states:

- status;
- purpose;
- public contract;
- fixture/method;
- failure ownership.

A new case is not valid merely because a new `check.py` exists. It must prove
a distinct public behavior not already covered elsewhere.

## Case status

| Case | Status | Role |
| --- | --- | --- |
| `workflow_case` | current | Normal reusable-workflow environment/authentication boundary. |
| `test_roots/001_simple` | current | Smallest standalone hello/timestamp consumer repository. |
| `test_roots/002_selection` | current | Changed-item selection across two items and one shared input. |
| `test_roots/003_fresh_runner` | current | Exact base/head selection from a clean clone. |
| `nested_item_case` | current | Nested item configuration and selection. |
| `nested_publish_case` | current | Nested durable output ownership. |
| `dependency_case` | current | Dependency fan-out and selected dependency execution. |
| `dependency_copy_case` | current | Engine-owned dependency-output copy. |
| `active_dependents_case` | current | Public direct-dependent command context. |
| `partial_rerun_case` | current | Public partial-run selectors. |
| `process_case` | current | Public item `process` participation semantics. |
| `parallel_jobs_case` | current | Public bounded `--jobs` behavior. |
| `directory_output_case` | current | Directory outputs and CacheDir restore/repair. |
| `timeout_case` | current | Timeout, override and command failure behavior. |
| `publish_case` | current | Durable build and Pages publication contract. |
| `merge_policy_case` | separate API | Merge governance, not CAD-CI execution; keep only while that API remains in `tool.cad.ci`. |

## Failure ownership

A current CAD-CI behavioral failure belongs in `tool.cad.ci` or
`lib.py.cad.ci`. Owner-level implementation/performance tests do not belong in
this external repository. Merge-governance failures belong to the owner of that
separate API.

Do not add another GitHub Actions job, tool bootstrap or parallel acceptance
architecture to accommodate a case.

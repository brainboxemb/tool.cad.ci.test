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
| `test_roots/004_nested_items` | current | Nested discovery, templates, path normalization and selection. |
| `test_roots/005_nested_publish` | current | Durable parent/nested-child output ownership and sparse updates. |
| `test_roots/006_dependencies` | current | Dependency traversal, fan-out and explicit downstream execution. |
| `test_roots/007_dependency_copy` | current | Engine-owned dependency-output copy and invalidation. |
| `test_roots/008_active_dependents` | current | Public direct-dependent selection context and target identity. |
| `test_roots/009_partial_rerun` | current | Public --step/--until/--from selector semantics. |
| `test_roots/010_process` | current | Public item-level process participation and exclusion. |
| `test_roots/012_parallel_jobs` | current | Public bounded --jobs concurrency using observable action intervals. |
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

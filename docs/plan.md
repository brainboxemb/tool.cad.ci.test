# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Baseline

- accepted baseline: `tool.cad.ci v0.23.0`;
- `v0.23.0` pins `lib.py.cad.ci 0.11.1`;
- simplified config-driven external acceptance passed in PR #94.

## Current work

### #95 — document and classify every acceptance case

1. give every registered top-level case a local README;
2. document purpose, public contract, fixture/method and failure ownership;
3. classify each case as current, transitional or separate API;
4. make `acceptance_suite/run.py` reject undocumented/obsolete registered cases;
5. keep current external black-box cases;
6. remove owner-level duplicate cases when equivalent owner coverage exists.

Owner-level duplicates removed in this issue:

- `logging_case`: live streaming is already covered in
  `lib.py.cad.ci/tests/test_scons_engine.py`;
- `selective_startup_case`: active-closure/symlink behavior is already covered
  in `lib.py.cad.ci/tests/test_scons_engine.py`.

Remaining special case:

- `merge_policy_case`: separate API; keep only while merge governance remains
  in `tool.cad.ci`.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #95 Document/classify acceptance cases | **now** | Finish README contract and merge after green acceptance. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance evidence only. Generic CI behavior and
owner-level implementation tests belong in the released library/tool
repositories.

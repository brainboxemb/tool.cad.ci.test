# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- previously accepted: `tool.cad.ci v0.24.0` /
  `lib.py.cad.ci 0.11.1`;
- candidate under #133: `tool.cad.ci v0.25.0` @
  `92b9cbb59bf24f6b47ba1fae267f67f2becc503f` with
  `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- v0.24.0 external acceptance passed in #102 / PR #104;
- config-driven acceptance architecture passed in PR #94;
- case ownership/documentation cleanup passed in PR #97.

## Current work

### #133 — declarative shared-builder acceptance

Qualify released v0.25.0 with `test_roots/011_shared_builder`. Prove two
items can share one repository-owned builder while their item `ci.yml` files
remain declarative.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using
`reusable-ci.yml@v0.24.0` and the released lane/merge policy.

### #106 — prove dev-cad to main promotion

Complete the current real promotion proof after the docs-only lane change.
Keep this as integration evidence; do not add another acceptance execution
route or duplicate generic merge/classification logic.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #133 v0.25.0 shared-builder acceptance | **now** | Run the full suite on v0.25.0 and prove test_roots/011_shared_builder. |
| #114 Migrate acceptance cases to numbered test roots | **active umbrella** | Continue incremental documented migrations; new normal cases go directly under test_roots/. |
| #106 dev-cad -> main promotion proof | **now / separate integration** | Finish the real promotion scenario and record resulting lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack. Every retained acceptance case stays locally documented and
must prove a distinct public contract.

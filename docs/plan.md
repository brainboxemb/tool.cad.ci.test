# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- accepted under #133 / PR #135: `tool.cad.ci v0.25.0` @
  `92b9cbb59bf24f6b47ba1fae267f67f2becc503f`;
- v0.25.0 pins `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- released-stack acceptance run #176 (`45063532187`) passed,
  including `test_roots/011_shared_builder`;
- config-driven acceptance architecture passed in PR #94;
- case ownership/documentation cleanup passed in PR #97;
- numbered standalone test roots proven on the integration lane:
  - `001_simple`;
  - `002_selection`;
  - `003_fresh_runner`;
  - `004_nested_items`;
  - `005_nested_publish`;
  - `006_dependencies`;
  - `007_dependency_copy`;
  - `008_active_dependents`;
  - `009_partial_rerun`;
  - `010_process`;
  - `011_shared_builder`;
  - `012_parallel_jobs`.

## Current work

### #139 — resolve v0.25 main -> dev-ci lane conflict

Combine the accepted v0.25/011 state from `main` with the numbered-root
migrations already on `dev-ci`, preserving both histories. Supersede
conflicted PR #137 after the resolution merge is complete.

### #114 — normalize remaining external cases into numbered test roots

Audit each remaining historical top-level case before migration. Retain only
distinct public consumer contracts, remove owner-level/obsolete duplicates, and
place retained standalone repositories below `test_roots/NNN_name/`.

The next normal candidate after synchronization is directory-output/cache
behavior; do not mechanically migrate special harness/governance cases.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using
`reusable-ci.yml@v0.25.0` and the released lane/merge policy.

### #106 — prove dev-cad to main promotion

Complete the real promotion proof after the docs-only lane change. Keep this as
integration evidence; do not add another acceptance execution route or
duplicate generic merge/classification logic.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #139 Resolve v0.25 main -> dev-ci conflict | **now** | Land the combined history-preserving lane state, then supersede #137. |
| #114 Numbered standalone test roots | **active umbrella** | Continue with the next distinct consumer use case after synchronization. |
| #106 dev-cad -> main promotion proof | **active integration** | Finish the real promotion scenario and record lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack. Every retained acceptance case stays locally documented and
must prove a distinct public contract.

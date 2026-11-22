# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- current released consumer target: `tool.cad.ci v0.27.1` @
  `716d22ce79551155b68413bd50fe3bf9d15d2254`;
- v0.27.1 pins `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- released-stack acceptance passed on v0.27.1 adoption PR #192;\n- stable-to-dev-ci synchronization PR #190 then succeeded through the fixed shared `/merge` path;
- branch-governance live acceptance is complete:
  - #180 / run `45070007017` proved conservative `/cleanup-branches`
    deletion and preservation of unique/unmerged history;
  - #186 / run `45071078228` retired the five separately reviewed
    unique-history refs through exact `(branch, SHA)` evidence;
- after #186 the stale historical set from the branch audit is gone; only
  permanent refs plus independently active concurrent work remain;
- v0.25/main + numbered dev-ci histories were reconciled by PR #140;
- numbered standalone test roots `001` through `012` are present on
  `dev-ci`;
- declarative builder migrations accepted on `dev-ci`:
  - `001_simple` — PR #143;
  - `002_selection` — PR #145;
  - `003_fresh_runner` — PR #147;
  - `004_nested_items` — PR #149;
  - `005_nested_publish` — PR #151;
  - `006_dependencies` — PR #153;
  - `007_dependency_copy` — PR #161;
  - `008_active_dependents` — PR #165;
  - `009_partial_rerun` — PR #177;
  - `010_process` — PR #179;
  - `011_shared_builder` — original canonical reference;
  - `012_parallel_jobs` — PR #183;
- acceptance timing observability landed in PR #159;
- non-failing timing budgets landed in PR #175.

## Current work

### #114 — normalize remaining external cases into numbered test roots

All existing numbered roots `001` through `012` satisfy the enforced
declarative builder architecture. #142/#184 are complete.

The remaining historical top-level cases have now been classified:

- `directory_output_case` — normal CAD-CI consumer; migrate as
  `013_directory_output` under #193;
- `timeout_case` — normal CAD-CI consumer; migrate after 013;
- `publish_case` — normal durable publication consumer; migrate after timeout;
- `workflow_case` — keep top-level as the outer reusable-workflow harness;
- `merge_policy_case` — keep top-level as a separately identified governance
  API harness.

Do not mechanically migrate the two special API harnesses.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using
`reusable-ci.yml@v0.27.1` and the released lane/merge policy.

### #106 — prove dev-cad to main promotion

Complete the real promotion proof after the docs-only lane change. Keep this as
integration evidence; do not add another acceptance execution route or
duplicate generic merge/classification logic.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #142 Declarative builder migration | **now** | `001`–`012` migrated; qualify durable architecture enforcement under #184, then close. |
| #114 Numbered standalone test roots | **blocked by #142 for normal roots** | Resume remaining top-level fixture migration after builder migration. |
| #106 dev-cad -> main promotion proof | **active integration** | Finish the real promotion scenario and record lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy, builder resolution and CAD-CI behavior
remain in the released tool/library stack.

Do not migrate Forge/CAD consumers to the builder model until this repository
proves the model across its existing numbered use cases.

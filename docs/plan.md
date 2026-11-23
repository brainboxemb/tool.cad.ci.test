# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Accepted baseline

- current released consumer target: `tool.cad.ci v0.28.0` @
  `805304b6a950319aed7dc8a77e9c7b501bb3fb61`;
- v0.28.0 pins `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- released-stack acceptance passed on v0.28.0 adoption PR #202;
- branch-governance live acceptance is complete:
  - #180 / run `45070007017` proved conservative `/cleanup-branches`
    deletion and preservation of unique/unmerged history;
  - #186 / run `45071078228` retired separately reviewed unique-history
    refs through exact `(branch, SHA)` evidence;
  - #200 / #203 / run `45075920227` proved reviewed
    `/merge-resolved` recovery for a genuinely conflicted permanent
    `main -> dev-cad` synchronization, with exact reviewed tree/parents;
- permanent-lane promotion proof #106 is complete:
  - docs-only PR #107 used the cheap lane-validation path;
  - promotion PR #204 forced full CAD-CI despite a docs-only tree delta;
  - merge commit `1e42ddb183c6e834b07e755862a165e891ec6cd6`
    advanced both `main` and `dev-cad`;
  - post-merge integration runs for both refs completed successfully;
- numbered standalone test roots `001` through `015` are present on
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
  - `011_shared_builder` — canonical shared-builder reference;
  - `012_parallel_jobs` — PR #183;
  - `013_directory_output` — PR #194;
  - `014_timeout` — PR #196;
  - `015_publish` — PR #198;
- acceptance timing observability landed in PR #159;
- non-failing timing budgets landed in PR #175;
- numbered-root normalization #114 is complete;
- permanent-lane integration #98 is complete under released v0.28.0:
  - conflicted `main -> dev-ci` PR #205 was recovered through reviewed
    `/merge-resolved` using green review PR #206;
  - resolved merge `a9406197e2f6cddfc0b1780b919d948ba3d7c16b`
    used reviewed tree `3cad750255cd3eb75145b8dd8f580c3c53e3c62d`;
  - dispatched dev-ci run `45132219820` passed;
  - promotion PR #207 was classified `lane-promotion`, forced
    `full_run=true`, and merged at
    `5da0adb401f8b680e2a44fa1780ccf61163fba7d`;
  - post-promotion runs `45132525063` (main) and `45132528589`
    (dev-ci) passed;
  - final main -> dev-cad sync PR #208 merged at
    `8ce1b656409501a428c765bc434e15bab9b62397`;
  - dev-cad contains current main with no file delta, and dispatched run
    `45132783513` passed.

## Current work

### #141 — external durable-lane workflow acceptance

This remains valid but is blocked on `brainboxemb/tool.cad.ci #137`.

The released v0.28.0 `reusable-ci.yml` is intentionally run-only and does not
yet expose the planned config-driven permanent-lane durable build/Pages
publication workflow. Do not emulate that missing surface locally in this test
repository.

When #137 reaches a released tool version, resume #141 with a numbered
standalone synthetic consumer and real stable/named durable publication
evidence before Forge or CAD adopt the new workflow.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #141 Durable-lane workflow acceptance | **blocked on tool.cad.ci #137** | Resume only after a released config-driven durable-lane workflow exists. |

## Completed normalization

Numbered-root normalization is complete under #114. All normal synthetic CAD-CI
consumer fixtures live below `test_roots/001` through `test_roots/015` and
are guarded by the declarative architecture validator. `workflow_case`
remains top-level because it accepts the outer reusable-workflow boundary;
`merge_policy_case` remains top-level as the separately identified
merge-governance API harness.

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy, builder resolution and CAD-CI behavior
remain in the released tool/library stack.

Do not migrate Forge/CAD consumers to the builder model until this repository
proves the model across its existing numbered use cases.

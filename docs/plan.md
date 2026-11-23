# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

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
- numbered-root normalization #114 is complete.

## Current work

### #98 — permanent lane integration

The `dev-cad` lane contract is fully accepted. The remaining closeout is the
`dev-ci` path:

1. synchronize current `main -> dev-ci` while preserving both permanent
   histories;
2. promote exact `dev-ci -> main` with complete CAD-CI;
3. verify the retained `dev-ci` lane advances to the stable merge commit and
   both post-merge integration runs are green;
4. synchronize the resulting stable `main` back into `dev-cad` so all three
   permanent source lanes finish aligned.

PR #205 is the current synchronization. It is genuinely conflicted, so use only
the released v0.28.0 reviewed `/merge-resolved` path; do not add a local
conflict workaround.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #98 Permanent lane integration | **now / closeout** | Resolve/sync PR #205, promote `dev-ci -> main`, then align `dev-cad` to final stable. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

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

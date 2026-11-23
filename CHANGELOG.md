# Changelog

Notable accepted changes to `tool.cad.ci.test`, newest first.

This repository is an external acceptance consumer, not a versioned package.
It has no GitHub releases, so historical entries use dated accepted-checkpoint
identifiers rather than invented repository versions.

## [Unreleased]

No notable unreleased acceptance changes are recorded.

## [permanent-lane-v0.28.0-acceptance] - 2026-11-23

### Infrastructure and tooling

- **Added:** completed live permanent-lane acceptance for `main`, `dev-ci`
  and `dev-cad` using released `tool.cad.ci v0.28.0`.
- **Added:** proved reviewed `/merge-resolved` recovery for a genuinely
  conflicted permanent `main -> dev-ci` synchronization, with immutable
  reviewed parents, resolution commit and tree.
- **Added:** proved direct `dev-ci -> main` promotion is classified as a lane
  promotion, forces complete CAD-CI, preserves the permanent lane and dispatches
  post-merge validation.
- **Changed:** synchronized the final stable tree back into both development
  lanes through the released history-preserving merge policy. The source lanes
  finish with the same repository tree while retaining their intended merge
  history.

### Documentation

- **Changed:** made `docs/plan.md` record immutable Actions/merge evidence for
  completed permanent-lane integration and explicitly mark the future durable
  publication acceptance as blocked on its owning tool work.

## [declarative-builder-normalization] - 2026-11-22

### Public API and behavior

- **Added:** normalized the external synthetic suite into standalone consumer
  roots `test_roots/001` through `test_roots/015`, covering selection,
  nested items, dependencies, partial reruns, process participation, bounded
  jobs, directory outputs, timeout/failure evidence and durable publication.
- **Changed:** normal executable item configurations became declarative
  consumer configuration selecting repository-owned builders; executable
  builder steps no longer live in item `ci.yml` files.
- **Added:** retained `workflow_case` and `merge_policy_case` as explicitly
  separate API harnesses instead of forcing GitHub workflow/governance behavior
  into synthetic numbered roots.

### Infrastructure and tooling

- **Added:** acceptance architecture validation prevents numbered roots from
  drifting back to inline executable item configuration.
- **Added:** non-failing per-case timing evidence and soft timing budgets for
  the complete released-stack acceptance suite.
- **Added:** live branch-governance acceptance for conservative stale-branch
  cleanup and separately reviewed exact-SHA branch retirement.
- **Changed:** adopted the released permanent-lane CI/merge policy instead of
  maintaining repository-local classification or merge logic.

## [released-stack-acceptance-expansion] - 2026-11-21

### Public API and behavior

- **Added:** accepted named durable build scopes and stable/named Pages
  publication while proving sibling scopes are preserved.
- **Added:** accepted same-runner consumer orchestration, dependency-output
  copying, bounded parallel jobs and selective-startup behavior through released
  tool/library stacks.

### Infrastructure and tooling

- **Changed:** continued converting the repository from isolated historical
  fixtures into one reusable-workflow consumer with explicit black-box cases.

## [reusable-workflow-acceptance] - 2026-11-19

### Public API and behavior

- **Added:** established this repository as the permanent external black-box
  consumer for released `tool.cad.ci` + `lib.py.cad.ci`.
- **Added:** proved cross-repository reusable workflow execution, caller context,
  public CLI behavior and GHCR authentication from a normal consumer.
- **Added:** accepted generated-build fetch, planner-derived selection and
  independent SCons-backed execution without importing implementation internals.

### Infrastructure and tooling

- **Changed:** moved acceptance toward the supported reusable workflow boundary
  rather than duplicating tool/library bootstrap in the consumer repository.

## [initial-synthetic-consumer] - 2026-11-18

### Public API and behavior

- **Added:** created the synthetic external consumer and initial durable
  build/Pages publication acceptance.
- **Added:** accepted directory step outputs and partial durable-main baseline
  updates through released public commands.

## Historical evidence notes

Checkpoint dates above are derived from repository commit/PR history. They
summarize meaningful accepted capability groups rather than reproducing every
historical tool-version pin or commit.

No repository package/release versions are inferred from the consumed
`tool.cad.ci` versions. Historical tool releases remain documented in the
owning `tool.cad.ci` changelog.

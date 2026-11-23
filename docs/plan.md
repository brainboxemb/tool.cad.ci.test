# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.30.0` @
  `5fcd77d5a07a68ef97cfcdb52b534f85bec1f1f2`;
- v0.30.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- numbered standalone test roots `001` through `016` are accepted;
- config-driven durable build/Pages and permanent-branch governance are proven
  live on the v0.30 baseline.

## Current released candidate

- `tool.cad.ci v0.31.0` @
  `27bdf67077ddd485cea95ba199069249c20c2a46`;
- v0.31.0 keeps the exact `lib.py.cad.ci 0.14.0` pin;
- runtime/merge/publication semantics are unchanged;
- public workflow configuration now uses literal names such as
  `stable_branch`, `development_branches`, `pull_request_policy` and
  `command_environment`.

## Current work

### #222 — external v0.31 workflow naming acceptance

**Now.** Prove the released v0.31 schema through real consumer workflows.

Required evidence:

1. real PR validation through `reusable-ci.yml@v0.31.0` using
   `pull_request_policy` and `command_environment`;
2. merge #222 adoption PR to permanent `dev-ci` through
   `reusable-merge-policy.yml@v0.31.0` with
   `stable_branch` / `development_branches` / `permanent_branches`;
3. post-merge `dev-ci` durable run green;
4. owner `/cleanup-branches` succeeds safely through the renamed cleanup
   inputs;
5. exact-SHA retirement of a deliberately missing temporary ref succeeds
   idempotently through the renamed retirement inputs;
6. `dev-ci -> main` promotion through v0.31 merge policy with both durable
   runs green;
7. `main -> dev-cad` synchronization through v0.31 merge policy with durable
   run green;
8. only then record v0.31.0 as fully accepted and close #222.

No new synthetic CAD behavior is required: the existing 001–016 suite is the
regression matrix for this schema-only release.

## Existing durable/governance evidence

- completed #141: v0.30 durable stable/named publication on reserved
  `test-output/*` refs;
- #180: conservative cleanup;
- #186: exact-SHA retirement;
- #200/#203: reviewed conflicted permanent sync recovery;
- #204/#207: permanent promotion proof;
- #205/#206/#208: permanent synchronization proof.

## Boundary

This repository owns external acceptance/integration evidence only. Generic
workflow behavior remains in the released tool/library stack.

Forge/CAD remain on their already reviewed consumer versions until #222 proves
the exact v0.31.0 workflow schema.

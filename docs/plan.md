# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.30.0` @
  `5fcd77d5a07a68ef97cfcdb52b534f85bec1f1f2`;
- v0.30.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- numbered standalone test roots `001` through `016` are accepted;
- merge governance, permanent-lane promotion/synchronization, conservative
  cleanup, exact-SHA retirement and reviewed conflict recovery have live GitHub
  evidence;
- the config-driven durable workflow is accepted end to end through completed
  issue #141.

## Durable workflow acceptance

Completed #141 proved both the synthetic consumer and real GitHub delivery
layers.

Key evidence:

- PR #216 candidate run `45142398079` (#259) passed against exact v0.30.0;
- isolated stable bootstrap run `45142533002` passed;
- PR #216 merged to permanent `dev-ci` at
  `34270607cc6afaa3b529a38821e9d1ef753eba65`;
- named `dev-ci` durable run `45142741953` passed;
- promotion PR #217 check `45142972524` passed;
- released merge policy produced history-preserving promotion commit
  `877bbc50e4d7073ad5e071a8571b8ac7086ea043` and advanced both
  `main` and `dev-ci`;
- post-promotion durable runs `45143126175` (main) and
  `45143130328` (dev-ci) passed;
- exact-SHA bootstrap retirement run `45143399322` passed.

Reserved live acceptance output remains on:

```text
test-output/build
test-output/gh-pages
```

Final #141 inspection proved stable `main` and named `dev-ci` build scopes,
stable and named Pages provenance, and preservation of the named Pages subtree
across the stable update. The repository's normal `build` and `gh-pages`
refs were never changed by this acceptance.

Detailed mutable provenance/run evidence is recorded on issue #141.

## Current work

No open acceptance/runtime issue.

Issue #218 only records this already accepted baseline in repository
documentation; it introduces no runtime behavior.

## Existing governance evidence

- #180 / run `45070007017`: conservative branch cleanup;
- #186 / run `45071078228`: reviewed exact-SHA retirement;
- #200 / #203 / run `45075920227`: reviewed conflicted permanent sync recovery;
- #204 and merge `1e42ddb183c6e834b07e755862a165e891ec6cd6`:
  lane-promotion full-run proof;
- #205/#206 and merge `a9406197e2f6cddfc0b1780b919d948ba3d7c16b`:
  reviewed main -> dev-ci conflict recovery;
- #207 promotion and runs `45132525063` / `45132528589`;
- #208 main -> dev-cad synchronization and run `45132783513`.

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy, builder resolution and CAD-CI behavior
remain in the released tool/library stack.

Forge/CAD may now consume the released v0.30.0 durable workflow; their own
repository migrations remain separately reviewed consumer work.

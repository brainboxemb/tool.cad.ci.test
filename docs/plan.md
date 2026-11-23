# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Accepted baseline

- current fully accepted consumer baseline remains `tool.cad.ci v0.28.0` @
  `805304b6a950319aed7dc8a77e9c7b501bb3fb61` until #141 completes;
- v0.29.0 compatibility of the pre-existing black-box suite was proven on
  PR #216, including run #255;
- numbered standalone test roots `001` through `015` are accepted on the
  permanent test lanes;
- branch governance, permanent-lane promotion/synchronization, conservative
  cleanup, exact-SHA retirement and reviewed conflict recovery already have
  live GitHub evidence from the completed scenarios recorded below.

## Current released candidate

- `tool.cad.ci v0.30.0` @
  `5fcd77d5a07a68ef97cfcdb52b534f85bec1f1f2`;
- v0.30.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- the released durable workflow now accepts generated branch names while
  preserving `build` and `gh-pages` defaults;
- PR #216 uses the isolated acceptance refs
  `test-output/build` and `test-output/gh-pages`.

## Current work

### #141 — external durable-lane workflow acceptance

**Now.** Finish the exact v0.30.0 released-stack acceptance.

The branch `issue/141-durable-lane-acceptance` must prove both layers:

1. numbered synthetic consumer `016_durable_workflow` with one normal build
   item, one site item and root `publication.pages` configuration;
2. real GitHub invocation of released `reusable-durable.yml` publishing only
   to the reserved `test-output/*` namespace.

Required live topology:

- bootstrap the isolated stable `main` scope before any named scope exists;
- publish permanent `dev-ci` as a named durable build/Page scope;
- promote `dev-ci -> main` through the released permanent-lane merge policy;
- prove the resulting stable publication preserves the named `dev-ci` Pages
  subtree;
- inspect exact source/build provenance in both generated refs;
- never use the repository's normal `build` or `gh-pages` refs for this
  acceptance.

Execution order:

1. make PR #216 green against exact v0.30.0, including test root 016;
2. create a short-lived live-scenario bootstrap source ref and run the released
   durable workflow with `scope=main` against `test-output/*`;
3. merge #216 to permanent `dev-ci`; require its push-triggered named durable
   run to pass;
4. open `dev-ci -> main` promotion PR and merge through released merge policy;
5. require stable and retained-lane durable runs to pass;
6. inspect `test-output/build` and `test-output/gh-pages` for exact stable
   and named provenance/preservation;
7. retire the bootstrap source ref after the real stable scope has replaced it;
8. close #141 and only then unblock Forge/CAD durable-workflow migration.

Do not add a local copy of the durable workflow or a test-only product input.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #141 Durable-lane workflow acceptance | **now** | Green PR #216 on v0.30.0, then execute isolated live stable/named publication and promotion proof. |

## Existing live evidence

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

Do not migrate Forge/CAD to the v0.30.0 durable workflow until #141 proves the
released public workflow end to end.

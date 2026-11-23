# 006 released durable workflow

Status: current

## Purpose

Prove the released `reusable-durable.yml` delivery layer with real GitHub
state while isolating generated acceptance output from the repository's normal
`build` and `gh-pages` refs.

## Contract

The scenario must use exact released `tool.cad.ci v0.30.0` and publish only to:

```text
test-output/build
test-output/gh-pages
```

Evidence must prove:

- a complete stable `main` build scope;
- a complete named `dev-ci` build scope;
- root stable Pages publication;
- a `dev-ci/` named Pages subtree;
- exact source/build provenance;
- a later stable publication preserves the named Pages subtree;
- the real reusable workflow performs the CAD-CI run and publication;
- no local copy of durable workflow logic, artifact handoff or consumer
  post-publication implementation exists.

## Method

Bootstrap the isolated stable `main` scope from a short-lived real source ref
using the released reusable durable workflow. Keep that source ref until the
real stable scope supersedes its source commit.

Then merge the accepted consumer update to permanent `dev-ci`, let its normal
push-triggered durable job publish the named scope, and promote `dev-ci` to
`main` through the released merge policy. Inspect the two reserved generated
refs after the stable update and record mutable run/commit evidence in issue
#141 / `docs/plan.md`.

The bootstrap ref is retired only after the real stable publication succeeds.

## Failure ownership

Workflow input/adapter behavior belongs in `tool.cad.ci`. Durable build-store,
Pages, freshness, provenance and generated-ref publication semantics belong in
`lib.py.cad.ci`.

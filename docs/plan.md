# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.32.0` @
  `19e894567ac534ce90428dc61c6afa126c1d3318`;
- v0.32.0 pins `lib.py.cad.ci 0.15.0` @
  `24c3abb267feea9ae91f24f8fdb435cba68f089a`;
- numbered standalone test roots `001` through `016` remain accepted;
- the real repository root now uses repository-owned builders rather than
  inline executable item steps:
  - `acceptance-suite` for the normal black-box graph;
  - `acceptance-pages` for post-build Pages rendering;
- live durable publication remains isolated on:
  - `test-output/build`;
  - `test-output/gh-pages`;
- normal `build` / `gh-pages` are not acceptance targets.

## v0.32 post-build Pages acceptance

Completed issue #232 proves `publication.pages.builder/output` through the
released durable workflow, not through library internals or a local workflow.

Key evidence:

- PR #233 black-box run #296 (`45160371055`) passed on exact v0.32.0;
- the initial named durable run #297 correctly exposed a bug only in the
  synthetic evidence assertion; durable build publication itself succeeded;
- follow-up PR #234 run #299 passed after aligning the evidence check with the
  documented durable manifest schema;
- named `dev-ci` durable run #300 (`45161204121`) passed at source
  `ae6eb8a6d4b43428a7c593a5f5fa09491dcb55f1`;
- that run published build commit
  `a0b3fc653e942d6570899eb1a645319be578d1df`, and the Pages builder received
  that exact commit through `CAD_CI_BUILD_COMMIT`;
- builder `context.json` and generic `provenance.json` agreed on source,
  build commit and named scope; root repository variable
  `ACCEPTANCE_MARKER=repository-config` overrode the caller value;
- promotion PR #235 run #301 passed; history-preserving promotion merge
  `74c5c2ba99175d8874fef93a7f90a6e1b593fc14` advanced both `main` and
  `dev-ci`;
- post-promotion durable runs #302 (main) and #303 (dev-ci) passed;
- stable Pages root uses build commit
  `2ab51467a1685f2337b42ff1799b6a58bbb48826`;
- the stable Pages commit preserved the then-current `dev-ci/` subtree
  exactly: tree `0ed0c5a7f28de34438b8ed7408f506bc2fa0cf8d` before and after the
  stable-root replacement;
- synchronization PR #236 run #304 passed; v0.32 merge-policy synchronized
  `main -> dev-cad` at
  `4d720c31958f78e9054c0f0d22e6d9fc24286aa4`;
- named `dev-cad` durable run #305 (`45162071702`) passed and published
  build commit `f3e75686d6a367f30f6333d803ef104445daa297` through the same
  post-build Pages builder.

## Current work

No open acceptance/runtime issue after #232 is closed.

## Existing evidence retained

- #141 / PR #216: durable workflow on reserved generated refs;
- #223 / PRs #225-#231: v0.31 public workflow names, promotion/sync,
  governance, exact-SHA retirement and cleanup;
- #232 / PRs #233-#236: v0.32 post-build Pages renderer, root builder
  structure and stable/named preservation.

## Boundary

This repository owns external acceptance evidence only. Generic builder
resolution, engine builders, post-build renderer execution, provenance,
selection and Pages publication remain in the released library/tool stack.

Consumers may adopt exact v0.32.0 for the accepted post-build Pages contract.
Generic built-in CAD engine builders remain separate future owner work in
`lib.py.cad.ci`.

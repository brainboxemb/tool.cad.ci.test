# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.32.0` @
  `19e894567ac534ce90428dc61c6afa126c1d3318`;
- v0.32.0 pins `lib.py.cad.ci 0.15.0` @
  `24c3abb267feea9ae91f24f8fdb435cba68f089a`;
- numbered standalone test roots `001` through `016` remain accepted;
- live durable publication remains isolated on `test-output/*`.

## Candidate stack under acceptance

### #240 — externally accept v0.33 built-in builders + verification

**Now.**

Candidate released stack:

- `tool.cad.ci v0.33.1` @
  `e319979fd6352ca6be2f95ff7227715f00253e96`;
- exact pinned `lib.py.cad.ci v0.17.1` @
  `00d0a763413650339945ca2d9bcfa4265e8dff35`;
- reusable verification engine `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- immutable generic runtime
  `ghcr.io/brainboxemb/cad-reference:v0.3.4`.

The new `test_roots/017_builtin_verification` must prove through only the
released public tool surface:

1. built-in build123d and CadQuery both export non-empty STL;
2. both mesh-geometry verification reports pass;
3. compatible verified models use one shared runtime batch;
4. an identical second run is CURRENT and does not start that runtime batch;
5. changing the shared verification definition affects both models and causes
   one shared batch rebuild;
6. all existing roots 001-016 and governance/publication acceptance remain
   green.

Repository wrappers are repinned to exact `v0.33.1`; no local workflow,
runtime launcher or CAD-CI implementation is added.

## Live acceptance sequence

1. Open #240 adoption PR to `dev-ci` and require the released v0.33 PR
   workflow green, including real GHCR/runtime execution.
2. Merge the short-lived branch to `dev-ci` through released merge policy.
3. Require the real named `dev-ci` durable run green on
   `test-output/build` / `test-output/gh-pages`.
4. Promote `dev-ci -> main` through the released history-preserving policy
   and require stable durable publication green.
5. Synchronize `main -> dev-cad` and require the named `dev-cad` durable
   run green.
6. Record exact mutable Actions/PR evidence, mark v0.33.1 fully accepted and
   close #240.

## Existing evidence retained

- #141 / PR #216: durable workflow on reserved generated refs;
- #223 / PRs #225-#231: v0.31 public workflow names, promotion/sync,
  governance, exact-SHA retirement and cleanup;
- #232 / PRs #233-#236: v0.32 post-build Pages renderer, root builder
  structure and stable/named preservation.

## Boundary

This repository owns external acceptance evidence only.

Minimal real build123d/CadQuery geometry is allowed only to exercise the
released generic built-in builder/runtime boundary. Generic builder resolution,
verification semantics, batching, provenance, selection and publication remain
in the released owner repositories. Forge, SolidCraft and product-model
semantics do not belong here.

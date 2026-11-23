# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.34.0` @
  `b1a2cf803bddb238ee50df29603f068488e72e5d`;
- exact pinned `lib.py.cad.ci v0.18.0` @
  `eb291abd6bb34b585d04019d154e7756d36436f9`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- numbered standalone roots 001 through 018 accepted;
- #244 completed external wildcard-prefix and repository-builder
  verification-package acceptance across dev-ci, main and dev-cad;
- live durable publication remains isolated on `test-output/*`.

## Candidate stack under acceptance

### #248 — accept v0.34.1 / lib 0.18.1 CadQuery Assembly export

**Now.**

Candidate released stack:

- `tool.cad.ci v0.34.1` @
  `e2ef58c1ff8cb2f9aacc2ddf28921cb62a28f625`;
- exact pinned `lib.py.cad.ci v0.18.1` @
  `6064a53b9ea1c340d49893ca0f8d1fa5e3e138ea`;
- reusable verification engine remains
  `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`.

New `test_roots/019_cadquery_assembly` must prove through only the released
public tool surface:

1. `builder: cadquery` executes a real minimal `cq.Assembly`;
2. the public output contains a non-empty `model.stl`;
3. the built-in batch reports the Assembly item as pass;
4. an identical rerun is CURRENT and does not restart the shared runtime batch.

Repository reusable CI/governance wrappers are repinned to exact v0.34.1 with
no copied generic implementation.

## Live acceptance sequence

1. require the #248 adoption PR to `dev-ci` green;
2. merge the short-lived branch through the released merge policy;
3. require named `dev-ci` durable integration green on
   `test-output/build` / `test-output/gh-pages`;
4. promote exact `dev-ci -> main` through released merge policy and require
   stable durable integration green;
5. synchronize exact `main -> dev-cad` and require named `dev-cad` durable
   integration green;
6. record exact mutable Actions/PR evidence, close #248 and return to Forge
   #740.

## Boundary

This repository owns external acceptance evidence only.

Do not add Forge/SolidCraft semantics, a local CadQuery exporter, library
imports, workflow bootstrap copies or a second CAD-CI graph. Generic failures
return to their owner repositories.

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

### #248 — accept v0.34.2 / lib 0.18.2 CadQuery Assembly export

**Now.**

Candidate released stack:

- `tool.cad.ci v0.34.2` @
  `37f7a82c6769279d33367144c56976da89bb1a5d`;
- exact pinned `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- reusable verification engine remains
  `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`.

The released pair must keep both existing and new CadQuery contracts green:

1. existing root 017 keeps normal CadQuery Workplane/Shape export green;
2. new `test_roots/019_cadquery_assembly` executes a real minimal `cq.Assembly`;
3. the public Assembly output contains a non-empty `model.stl`;
4. the built-in batch reports the Assembly item as pass;
5. identical reruns remain CURRENT and do not restart the shared runtime batch.

Repository reusable CI/governance wrappers are repinned to exact v0.34.2 with
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

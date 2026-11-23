# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.33.2` @
  `4812d87304109a68538d844e8baa5bacdbbc198d`;
- exact pinned `lib.py.cad.ci v0.17.2` @
  `d4e8140d988be06460326fda802e514b6b306d64`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- numbered standalone roots 001 through 017 accepted;
- #240 completed real built-in build123d/CadQuery verification acceptance plus
  permanent dev-ci/main/dev-cad durable promotion/synchronization;
- live durable publication remains isolated on `test-output/*`.

## Candidate stack under acceptance

### #244 — accept v0.34.0 / lib 0.18.0 owner contracts

**Now.**

Candidate released stack:

- `tool.cad.ci v0.34.0` @
  `b1a2cf803bddb238ee50df29603f068488e72e5d`;
- exact pinned `lib.py.cad.ci v0.18.0` @
  `eb291abd6bb34b585d04019d154e7756d36436f9`;
- reusable verification engine `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`.

New `test_roots/018_builder_verification_package` must prove through only the
released public tool surface:

1. a repository-owned builder declares `verification_package: true`;
2. root configuration pins the exact released verification package;
3. the command receives an existing exact `CAD_CI_VERIFICATION_WHEEL`;
4. consumer configuration never names the synthesized package item id;
5. an identical rerun is CURRENT;
6. `models/*/scpf/**` correctly selects the nested model for a changed path.

Repository reusable CI and merge-policy wrappers are repinned to exact v0.34.0
without copying generic implementation.

## Live acceptance sequence

1. require the #244 adoption PR to `dev-ci` green;
2. merge the short-lived branch through the released merge policy;
3. require named `dev-ci` durable integration green on
   `test-output/build` / `test-output/gh-pages`;
4. promote exact `dev-ci -> main` through released merge policy and require
   stable durable integration green;
5. synchronize exact `main -> dev-cad` and require named `dev-cad` durable
   integration green;
6. record exact mutable Actions/PR evidence, close #244 and return to Forge
   #740.

## Boundary

This repository owns external acceptance evidence only.

Do not add Forge/SolidCraft semantics, library imports, internal package ids,
local verification package download logic, workflow bootstrap copies or a
second CAD-CI graph. Generic failures return to their owner repositories.

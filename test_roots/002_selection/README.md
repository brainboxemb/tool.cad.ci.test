# 002 changed-item selection

Status: current

## Purpose

Standalone consumer repository for changed-path selection.

## Public contract

This test root proves that coarse Git/change-path selection is independent from
SCons target freshness:

1. a cold run builds alpha and beta;
2. `plan --changed alpha/input.txt` selects alpha only;
3. changing alpha input and running with that changed path rebuilds alpha only;
4. `plan --changed shared.txt` selects both items;
5. changing the shared input rebuilds both items.

## Fixture

`cad-ci.yml` configures two items, `alpha` and `beta`. Both watch
`shared.txt`; each also owns its own input.

## Failure ownership

Changed-path selection/configuration belongs in `lib.py.cad.ci`.

Do not add explicit base/head fresh-runner selection here. That is a separate
consumer use case.

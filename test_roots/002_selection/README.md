# 002 changed-item selection

Status: current

## Purpose

Standalone consumer repository for changed-path selection using one shared
repository-owned builder.

## Public contract

This test root proves that coarse Git/change-path selection is independent from
SCons target freshness:

1. a cold run builds alpha and beta;
2. `plan --changed alpha/input.txt` selects alpha only;
3. changing alpha input and running with that changed path rebuilds alpha only;
4. `plan --changed shared.txt` selects both items;
5. changing the shared input rebuilds both items.

## Declarative builder contract

`cad-ci.yml` defines one builder alias:

```yaml
builders:
  selection: ci/builders/selection
```

Both `alpha/ci.yml` and `beta/ci.yml` contain only item identity, builder
selection and watch configuration. They contain no executable `steps:` or
`run:`.

The shared builder owns the item-local `input.txt`, repository-level
`shared.txt`, execution command and `result.txt` output.

## Failure ownership

Changed-path selection/configuration and builder resolution belong in
`lib.py.cad.ci`.

Do not add explicit base/head fresh-runner selection here. That is a separate
consumer use case in `003_fresh_runner`.

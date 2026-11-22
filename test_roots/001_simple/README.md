# 001 simple build

Status: current

## Purpose

Smallest end-to-end consumer repository in the external acceptance suite.

## Repository contract

This directory is a self-contained synthetic consumer repository. Its item
configuration is declarative; executable behavior lives in a repository-owned
builder.

```text
001_simple/
  cad-ci.yml
  ci.yml
  hello.md
  check.py
  ci/
    builders/
      simple/
        builder.yml
        build.py
```

## Public contract

The case proves only:

1. the repository's own `cad-ci.yml` loads;
2. the repository root itself can be the configured item;
3. the root item selects `builder: simple` without inline `steps:` or `run:`;
4. a cold run executes the repository-owned builder;
5. `build/hello.md` contains the source plus a UTC build timestamp;
6. an unchanged second run is current and does not rewrite the timestamp;
7. changing source `hello.md` rebuilds the item and writes a new timestamp.

## Fixture

`hello.md` is the only meaningful item input. The `simple` builder owns the
build command, declared inputs/outputs and implementation script.

Builder implementation changes are automatically part of the builder watch
contract supplied by `lib.py.cad.ci`.

## Failure ownership

Builder resolution/configuration/execution/currentness belongs in
`lib.py.cad.ci`. Public CLI invocation belongs in `tool.cad.ci`.

Do not add dependencies, publication, cache-recovery or multiple items here.
Those belong in separate numbered test roots.

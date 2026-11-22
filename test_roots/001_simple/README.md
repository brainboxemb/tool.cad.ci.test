# 001 simple build

Status: current

## Purpose

Smallest end-to-end consumer repository in the external acceptance suite.

## Repository contract

This directory is a self-contained synthetic consumer repository. It owns its
own root `cad-ci.yml` and root item `ci.yml`.

```text
001_simple/
  cad-ci.yml
  ci.yml
  hello.md
  build.py
  check.py
```

## Public contract

The case proves only:

1. the repository's own `cad-ci.yml` loads;
2. the repository root itself can be the configured item;
3. a cold run executes one configured build;
4. `build/hello.md` contains the source plus a UTC build timestamp;
5. an unchanged second run is current and does not rewrite the timestamp;
6. changing source `hello.md` rebuilds the item and writes a new timestamp.

## Fixture

`hello.md` is the only meaningful source input. `build.py` copies its content
to the configured output and appends `Built at: <UTC timestamp>`.

## Failure ownership

Configuration/execution/currentness belongs in `lib.py.cad.ci`. Public CLI
invocation belongs in `tool.cad.ci`.

Do not add dependencies, publication, cache-recovery or multiple items here.
Those belong in separate numbered test roots.

# 003 fresh-runner selection

Status: current

## Purpose

Standalone consumer repository for explicit Git base/head selection on a clean
runner using one shared declarative builder.

## Public contract

The case proves:

1. a base commit contains items `a` and `b`;
2. the head changes only `a`;
3. a fresh clone has no previous build or CAD-CI state;
4. `plan --base <base> --head <head>` selects only `a`;
5. `run --base <base> --head <head>` builds only `a`;
6. no output for `b` is materialized.

## Declarative builder contract

`cad-ci.yml` maps `builder: item` to `ci/builders/item`.

Both item `ci.yml` files contain only identity, builder selection and
item-local watch configuration. They contain no executable `steps:` or
`run:`.

The shared builder owns `input.txt`, the execution command and
`result.txt` output.

## Fixture

The check creates local Git history inside the disposable copy, then clones that
repository again before invoking the public CLI.

## Failure ownership

Exact Git base/head selection, builder resolution and execution belong in
`lib.py.cad.ci`.

Do not add ordinary changed-path selection here; that is
`test_roots/002_selection`.

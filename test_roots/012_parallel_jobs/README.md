# 012 parallel jobs

Status: current

## Purpose

Standalone consumer repository for the public bounded `--jobs` surface using
one shared declarative builder.

## Public contract

The case proves:

1. `--jobs 2` is accepted by the released CLI;
2. two independent configured actions both complete successfully;
3. public step evidence records successful executed actions;
4. the two public action timestamp intervals overlap.

The overlap is the behavioral proof of concurrent execution. This is not a
benchmark and does not inspect private scheduler/SCons internals.

## Declarative builder contract

Both `left` and `right` select the same repository-owned `parallel`
builder and keep only item-local `input.txt` watch configuration.

The builder owns the `build` step, deliberate short sleep, execution command
and `result.txt` output. Item configs contain no executable `steps:` or
`run:`.

The sleep exists only to make overlapping public action intervals observable;
case duration is monitored separately by the central acceptance timing
contract.

## Failure ownership

Parallel execution belongs in `lib.py.cad.ci`; `--jobs` CLI forwarding
belongs in `tool.cad.ci`.

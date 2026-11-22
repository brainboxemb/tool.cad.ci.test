# 012 parallel jobs

Status: current

## Purpose

Standalone consumer repository for the public bounded `--jobs` surface.

## Public contract

The case proves:

1. `--jobs 2` is accepted by the released CLI;
2. two independent configured actions both complete successfully;
3. public step evidence records successful executed actions;
4. the two public action timestamp intervals overlap.

The overlap is the behavioral proof of concurrent execution. This is not a
benchmark and does not inspect private scheduler/SCons internals.

## Fixture

The repository has two independent items, `left` and `right`. Each action
sleeps briefly before writing one declared output so overlap is observable in
public evidence.

## Failure ownership

Parallel execution belongs in `lib.py.cad.ci`; `--jobs` CLI forwarding
belongs in `tool.cad.ci`.

# 007 dependency output copy

Status: current

## Purpose

Standalone consumer repository for the public engine-owned dependency `copy`
action using declarative repository-owned builders.

## Public contract

The case proves:

1. a producer builds one output tree;
2. two consumers materialize selected dependency output without consumer copy
   scripts;
3. public step evidence reports `action_type: copy` and `BUILT` on a cold run;
4. an unchanged rerun reports `CURRENT` without executing the copy action;
5. changing producer input rebuilds the producer and both copy targets;
6. copied consumer output reflects the changed producer data.

## Declarative builder contract

`cad-ci.yml` defines two builder aliases:

- `batch` owns the producer command and output tree;
- `materialize` owns the engine-native `copy:` action.

The consumer item `ci.yml` files contain only identity/kind,
`builder: materialize` and `needs: [batch]`. They contain no `steps:`,
`run:` or `copy:`.

Consumers still contain no Python/action scripts.

## Failure ownership

Dependency copy modeling, invalidation, builder resolution and execution belong
in `lib.py.cad.ci`.

Ordinary dependency traversal/fan-out is covered by
`test_roots/006_dependencies`.

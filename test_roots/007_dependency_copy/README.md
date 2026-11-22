# 007 dependency output copy

Status: current

## Purpose

Standalone consumer repository for the public engine-owned dependency `copy`
step.

## Public contract

The case proves:

1. a producer builds one output tree;
2. two consumers materialize selected dependency output without consumer copy
   scripts;
3. public step evidence reports `action_type: copy` and `BUILT` on a cold run;
4. an unchanged rerun reports `CURRENT` without executing the copy action;
5. changing producer input rebuilds the producer and both copy targets;
6. copied consumer output reflects the changed producer data.

## Fixture

`batch` produces per-consumer files below one declared output tree.
`consumer-a` and `consumer-b` contain no Python/script action; their
`materialize` step is configured only with `copy:`.

## Failure ownership

Dependency copy modeling, invalidation and execution belong in
`lib.py.cad.ci`.

Ordinary dependency traversal/fan-out is covered by
`test_roots/006_dependencies`.

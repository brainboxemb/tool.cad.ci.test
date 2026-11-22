# 006 dependencies

Status: current

## Purpose

Standalone consumer repository for public dependency traversal and fan-out
using declarative repository-owned builders.

## Public contract

The case proves:

1. a cold run builds a producer, two consumers and a downstream summary;
2. the producer keeps ordered public steps `prepare` and `finish`;
3. an unrelated consumer-only change rebuilds only that consumer;
4. changing the producer rebuilds the producer and both direct consumers;
5. the downstream summary is not implicitly selected by that producer change;
6. explicitly running the summary makes its consumer prerequisites current
   before the summary target executes.

## Declarative builder contract

`cad-ci.yml` defines three builder aliases:

- `library` owns ordered `prepare` and `finish` steps;
- `consumer` is shared by consumer-a and consumer-b;
- `summary` owns downstream aggregation.

Item `ci.yml` files contain only identity/kind, builder selection,
dependencies, watch configuration and summary strategy. They contain no
executable `steps:` or `run:`.

## Fixture

`library` is the producer. `consumer-a` and `consumer-b` depend on it.
`summary` depends on both consumers.

## Failure ownership

Dependency graph selection, builder resolution and SCons prerequisite execution
belong in `lib.py.cad.ci`.

Dependency-output copying is intentionally a separate consumer contract in
`007_dependency_copy`.

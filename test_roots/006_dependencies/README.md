# 006 dependencies

Status: current

## Purpose

Standalone consumer repository for public dependency traversal and fan-out.

## Public contract

The case proves:

1. a cold run builds a producer, two consumers and a downstream summary;
2. an unrelated consumer-only change rebuilds only that consumer;
3. changing the producer rebuilds the producer and both direct consumers;
4. the downstream summary is not implicitly selected by that producer change;
5. explicitly running the summary makes its consumer prerequisites current
   before the summary target executes.

## Fixture

`library` is the producer. `consumer-a` and `consumer-b` depend on it.
`summary` depends on both consumers.

## Failure ownership

Dependency graph selection and SCons prerequisite execution belong in
`lib.py.cad.ci`.

Dependency-output copying is intentionally a separate consumer contract.

# Process participation case

Status: current

## Purpose

Prove the public item-level `process` configuration.

## Public contract

Omitted/`true` items participate in normal full planning/execution;
`process: false` items are excluded from normal processing and reject
explicit execution.

## Fixture and method

The synthetic repository contains default-active, explicit-active and disabled
items and observes public plan/run/build-store behavior.

## Failure ownership

The `process` configuration contract belongs in `lib.py.cad.ci`. If that
feature is retired, this case must be retired with it rather than preserved as
historical behavior.

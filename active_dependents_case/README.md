# Active dependents case

Status: current

## Purpose

Prove public `selection_context: direct_dependents` behavior.

## Public contract

A shared producer receives the active direct-dependent set for the current
selection, and that context participates in target identity/evidence.

## Fixture and method

Two consumers depend on one batch item. The case executes one consumer, the
other, both through change selection, and a full run.

## Failure ownership

Selection context and SCons target signatures belong in `lib.py.cad.ci`.

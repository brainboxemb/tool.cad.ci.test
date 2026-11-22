# Simple execution case

Status: current

## Purpose

Provide the smallest released-stack proof of SCons-backed build/current
behavior and step-input invalidation.

## Public contract

A cold run builds configured steps; an unchanged rerun reports them current;
changing only verify input reruns verify; changing build input membership
invalidates the required targets.

## Fixture and method

The case copies its tiny consumer repository to disposable output and invokes
the public CLI repeatedly while mutating only declared inputs.

## Failure ownership

Execution/rebuild semantics belong in `lib.py.cad.ci`; CLI exposure belongs in
`tool.cad.ci`.

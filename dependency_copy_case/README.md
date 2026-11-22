# Dependency-output copy case

Status: current

## Purpose

Prove the public engine-owned `copy` step without consumer copy scripts.

## Public contract

Dependency outputs are copied to consumers, current/rebuild behavior is
recorded in public step evidence, and copy steps remain engine-owned.

## Fixture and method

One producer feeds two copy-only consumers. The case checks generated files and
public evidence before and after dependency changes.

## Failure ownership

Copy-step modeling/execution belongs in `lib.py.cad.ci`.

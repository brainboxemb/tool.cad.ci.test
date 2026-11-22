# 010 process participation

Status: current

## Purpose

Standalone consumer repository for the public item-level `process`
configuration.

## Public contract

The case proves:

1. an item with omitted `process` participates by default;
2. `process: true` participates explicitly;
3. `process: false` is excluded from normal plan/run;
4. disabled items do not produce build output/evidence or durable main output;
5. explicitly requesting a disabled item is rejected through the public CLI.

## Fixture

The repository contains `default_active`, `explicit_active` and `disabled`
items with otherwise equivalent build steps.

## Failure ownership

The public `process` configuration contract belongs in `lib.py.cad.ci`.

If the public field is retired, remove this test root instead of preserving
historical behavior.

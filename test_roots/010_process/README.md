# 010 process participation

Status: current

## Purpose

Standalone consumer repository for the public item-level `process`
configuration using one shared declarative builder.

## Public contract

The case proves:

1. an item with omitted `process` participates by default;
2. `process: true` participates explicitly;
3. `process: false` is excluded from normal plan/run;
4. disabled items do not produce build output/evidence or durable main output;
5. explicitly requesting a disabled item is rejected through the public CLI.

## Declarative builder contract

All three items select the same repository-owned `process` builder.

The item configs differ only in identity, watch configuration and the public
`process` field. They contain no executable `steps:` or `run:`.

The builder owns the single `build` step and `result.txt` implementation.
Process participation remains item configuration; it is not builder behavior.

## Failure ownership

The public `process` configuration contract and builder resolution belong in
`lib.py.cad.ci`.

If the public field is retired, remove this test root instead of preserving
historical behavior.

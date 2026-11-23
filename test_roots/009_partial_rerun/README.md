# 009 partial rerun

Status: current

## Purpose

Standalone consumer repository for the public partial-run selectors using a
declarative multi-step builder.

## Public contract

The case proves:

1. a complete run executes all configured steps and writes complete item
   evidence;
2. `--step build` makes prerequisites current, forces only `build`, skips
   later steps and leaves no complete-item evidence;
3. `--until build` stops after `build` and leaves no complete-item evidence;
4. `--from build` keeps earlier prerequisites current, forces `build` and the
   following step, then restores complete-item evidence.

## Declarative builder contract

The item `ci.yml` contains only identity, kind and `builder: partial`.

The repository-owned builder defines the ordered public step names:

1. `prepare`;
2. `build`;
3. `verify`.

Those names intentionally remain public because the CLI selectors address
builder steps by name. Moving the steps into the builder must not rename or
hide them.

The builder owns the commands, implementation scripts and declared outputs.
The item configuration contains no executable `steps:` or `run:`.

## Failure ownership

Partial-run selector semantics and builder step ordering belong in
`lib.py.cad.ci`; CLI argument forwarding belongs in `tool.cad.ci`.

Timeout/failure behavior is intentionally separate.

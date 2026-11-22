# 009 partial rerun

Status: current

## Purpose

Standalone consumer repository for the public partial-run selectors.

## Public contract

The case proves:

1. a complete run executes all configured steps and writes complete item
   evidence;
2. `--step build` makes prerequisites current, forces only `build`, skips
   later steps and leaves no complete-item evidence;
3. `--until build` stops after `build` and leaves no complete-item evidence;
4. `--from build` keeps earlier prerequisites current, forces `build` and the
   following step, then restores complete-item evidence.

## Fixture

One item contains three ordered steps: `prepare`, `build`, `verify`.

## Failure ownership

Partial-run selector semantics belong in `lib.py.cad.ci`; CLI argument
forwarding belongs in `tool.cad.ci`.

Timeout/failure behavior is intentionally separate.

# Partial rerun case

Status: current

## Purpose

Prove the public meanings of `--step`, `--until` and `--from`.

## Public contract

Exact-step execution makes prerequisites current without completing later
steps; `--until` stops at the named step; `--from` forces that step and the
following configured steps. Complete item evidence exists only for complete
runs.

## Fixture and method

A three-step item is run normally and with each public selector.

## Failure ownership

Selector semantics belong in `lib.py.cad.ci`; CLI argument forwarding belongs
in `tool.cad.ci`.

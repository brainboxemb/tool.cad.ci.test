# Parallel jobs case

Status: current

## Purpose

Prove the public bounded `--jobs` surface actually enables concurrent
independent SCons actions.

## Public contract

`--jobs 2` executes two independent targets successfully and their public
action timestamp intervals overlap.

## Fixture and method

A generated two-item repository runs two deliberate short actions; only public
step evidence is inspected.

## Failure ownership

Parallel execution belongs in `lib.py.cad.ci`; CLI forwarding belongs in
`tool.cad.ci`.

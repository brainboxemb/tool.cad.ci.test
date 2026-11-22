# Fresh-runner selection case

Status: current

## Purpose

Prove exact base/head Git selection from a clean clone with no previous build
or SCons state.

## Public contract

Given explicit base/head commits, only the changed item is selected and built
on a fresh runner.

## Fixture and method

The case creates a local Git history, clones it fresh and invokes the public
plan/run interfaces with exact revisions.

## Failure ownership

Git selection and execution semantics belong in `lib.py.cad.ci`.

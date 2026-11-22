# Logging case

Status: transitional — candidate for removal from external acceptance

## Purpose

Prove that consumer command output is streamed live and that CLI output remains
concise.

## Why transitional

This primarily tests CLI presentation/process streaming owned by
`tool.cad.ci`, not cross-repository CAD-CI behavior. It should move to the
tool repository's own CLI tests once equivalent owner coverage is confirmed.

## Fixture and method

The case starts `python -m cad_ci_tool run`, reads stdout while the process is
still running and checks that early consumer output is visible.

## Failure ownership

`tool.cad.ci`. Do not add more external acceptance around logging details.

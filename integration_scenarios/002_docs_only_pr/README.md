# 002 docs-only PR

Status: current

## Purpose

Prove the released documentation-only cheap path on a permanent development
lane.

## Real execution

1. create a short-lived branch from current `dev-ci` or `dev-cad`;
2. change only files below `docs/**`;
3. open a pull request to that development lane;
4. observe a real `pull_request` Actions event.

## Acceptance

The released classifier must identify a non-empty docs-only diff and complete
the cheap validation path before Python/tool/library/CAD-CI bootstrap.

The Actions run must show the expensive bootstrap/execution steps skipped.

No local classifier is allowed in this repository.

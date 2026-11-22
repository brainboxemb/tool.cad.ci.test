# 003 lane promotion

Status: current

## Purpose

Prove a real permanent development-lane promotion to stable `main`.

## Real execution

1. ensure the development lane contains accepted work;
2. open the exact PR `dev-ci -> main` or `dev-cad -> main`;
3. observe the real `pull_request` workflow;
4. require complete CAD-CI even when the lane delta is documentation-only;
5. after green validation, issue the real owner `/merge` command.

## Acceptance

The released merge policy must use history-preserving merge behavior, keep the
permanent lane, and advance stable history without squash-flattening the lane.

Post-merge integration validation must be dispatched through the normal
workflow.

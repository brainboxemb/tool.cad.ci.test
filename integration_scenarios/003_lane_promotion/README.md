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

## Current-release qualification

The promotion must exercise the currently accepted release from the default
branch. Before `/merge`, verify that `main` loads the same released merge-policy
version used by the lane CI. Historical success on an older merge-policy
release is not sufficient.

The lane delta used for the probe must first arrive through a normal accepted
short-lived PR into the development lane; do not manufacture the promotion by
directly editing the permanent lane.

## Acceptance

The released merge policy must use history-preserving merge behavior, keep the
permanent lane, and advance stable history without squash-flattening the lane.

Post-merge integration validation must be dispatched through the normal
workflow.

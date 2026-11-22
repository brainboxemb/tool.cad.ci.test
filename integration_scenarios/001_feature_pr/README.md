# 001 feature PR

Status: current

## Purpose

Prove the normal GitHub consumer path for a short-lived non-documentation
branch targeting a permanent development lane.

## Real execution

1. create a short-lived branch from current `dev-ci`;
2. make a non-`docs/**` change;
3. open a pull request to `dev-ci`;
4. observe a real `pull_request` Actions event;
5. verify `reusable-ci.yml@v0.25.0` is invoked;
6. verify the full acceptance graph runs;
7. squash-merge the short-lived branch.

## Acceptance

The scenario passes only when the GitHub Actions run is successful and the PR
is merged through the normal short-lived-work policy.

A local CLI run is not evidence for this scenario.

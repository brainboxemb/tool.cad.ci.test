# 004 stable-to-lane synchronization

Status: current

## Purpose

Prove real synchronization from stable `main` back into a permanent
development lane.

## Real execution

1. advance `main` independently of the target lane;
2. open the exact PR `main -> dev-ci` or `main -> dev-cad`;
3. complete normal PR validation;
4. issue the real owner `/merge` command.

## Acceptance

The released merge policy must preserve history, keep the permanent lane
present after merge, and dispatch `ci.yml` after integration.

The dispatched `workflow_dispatch` run must execute complete acceptance.

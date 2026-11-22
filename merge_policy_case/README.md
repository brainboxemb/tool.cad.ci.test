# Merge policy case

Status: separate API — temporary in this repository

## Purpose

Accept the merge-governance API currently shipped by `tool.cad.ci`.

## Why separate

Merge governance is not CAD-CI execution. It remains here only because
`tool.cad.ci` currently publishes that API and there is no separate
acceptance repository for it.

## Public contract

The case checks durable-lane merge decisions and executes the released merge
command against a fake GitHub API for refusal, unknown outcome, post-merge
failure and successful merge scenarios.

## Fixture and method

`check.py` observes the released policy helper/workflow contract.
`check_command.py` supplies a temporary fake `gh` executable so no live
GitHub mutation occurs.

## Failure ownership

The merge-governance owner. When that API moves or is removed, this entire case
must move/remove with it.

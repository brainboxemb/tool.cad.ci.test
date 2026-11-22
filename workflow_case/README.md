# Workflow case

Status: current

## Purpose

Prove the normal released reusable-workflow boundary from a real consumer
command.

## Public contract

- root repository variables reach the consumer command;
- repository values override inherited non-secret caller values;
- GHCR authentication is available before consumer CAD-CI commands run.

## Fixture and method

The outer repository is already running through `reusable-ci.yml`.
`workflow_case/ci.yml` executes `check.py`, which checks only the observable
environment and Docker configuration and writes one result file.

## Failure ownership

Workflow bootstrap/authentication failures belong in `tool.cad.ci`.
Repository-variable semantics belong in `lib.py.cad.ci`.

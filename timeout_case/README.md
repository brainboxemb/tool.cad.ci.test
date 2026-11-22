# Timeout and failure case

Status: current

## Purpose

Prove repository-default timeouts, per-step overrides and ordinary command
failure reporting.

## Public contract

Timeout and failure states produce the documented exit behavior and public
evidence; a larger step override succeeds.

## Fixture and method

Three small items intentionally time out, override the timeout, or exit with a
known failure code.

## Failure ownership

Timeout/execution evidence belongs in `lib.py.cad.ci`.

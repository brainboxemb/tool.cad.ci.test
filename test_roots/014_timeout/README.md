# 014 timeout and failure

Status: current

## Purpose

Standalone consumer repository for repository-default timeouts, step-level
timeout overrides and ordinary command failures using declarative
repository-owned builders.

## Public contract

The case proves:

1. the repository default timeout terminates a long-running action;
2. timeout evidence reports `timeout` / `ERROR` with no complete item evidence;
3. a larger step-level timeout override succeeds and produces complete evidence;
4. an ordinary command exit code 3 reports `fail` / `ERROR` without complete
   item evidence.

The check reads only public evidence and invokes only the released public CLI.

## Declarative builder contract

The three item configs contain identity, kind and builder selection only.

- `timeout-default` owns the long-running command and inherits the repository
  default timeout;
- `timeout-override` owns the same public step with an explicit 3 second
  step-level override;
- `command-failure` owns the command that deliberately exits with code 3.

Executable `steps:` / `run:` and implementation scripts live only below
`ci/builders/`.

## Failure ownership

Timeout, command execution and public evidence semantics belong in
`lib.py.cad.ci`.

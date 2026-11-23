# Repository-builder verification package acceptance

Status: current

## Purpose

Black-box the released public verification-package capability for a
repository-owned builder and the wildcard-aware recursive path matcher.

## Public contract

- root `verification.package` pins one exact released verification library;
- repository builder `verification_package: true` requests that package;
- the builder command receives `CAD_CI_VERIFICATION_WHEEL`;
- normal item configuration does not describe package materialization;
- identical reruns remain CURRENT;
- wildcard prefixes before trailing `/**` participate in changed-path
  selection.

## Fixture / method

One synthetic item lives at `models/a`. Its repository-level watch pattern is
`models/*/scpf/**`. The shared builder reads only the public wheel environment
value, validates wheel metadata with the Python standard library and writes a
small JSON result.

The case invokes only the public released `cad-ci` CLI.

## Failure ownership

Configuration, path matching, package materialization, dependency wiring and
command environment failures belong to `lib.py.cad.ci`. Reusable workflow
bootstrap/release loading failures belong to `tool.cad.ci`.

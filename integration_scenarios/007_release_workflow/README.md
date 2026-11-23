# 007 central CAD release workflow

Status: current

## Purpose

Prove released `tool.cad.ci v0.36.0` release behavior with real GitHub
issue comments and generated build state.

## Contract

The consumer uses the copy-ready `cad-release` wrapper and changes only the
generated build branch to the reserved acceptance ref:

```text
test-output/build
```

Release qualification must read the stable main ci-build-record from:

```text
test-output/build:main/build.json
```

It must not use `gh-pages` or `test-output/gh-pages` as release evidence.

## Method

After v0.36.0 adoption reaches `main` and the main durable workflow is green:

1. issue a real owner `/release` comment for an older main SHA;
2. require the central CAD build check to reject it before release creation;
3. issue the same version for the exact current main SHA;
4. require the CAD check and delegated `tool.py.lib.ci` release transaction
   to succeed;
5. verify the resulting tag/GitHub Release points to the exact main SHA;
6. repeat the successful command and require idempotent success.

Mutable PR, Actions, issue-comment and release evidence is recorded on #256.

## Failure ownership

Stable build-record semantics belong in `lib.py.cad.ci`. The CAD release
workflow/template belongs in `tool.cad.ci`. Generic tag/GitHub Release
mechanics belong in `tool.py.lib.ci`. This test repository adds no local
replacement for any of those layers.

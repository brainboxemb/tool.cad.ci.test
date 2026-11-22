# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22). This repository is the permanent external black-box acceptance
repository and owns no CAD-CI algorithms.

## Accepted baseline

- `tool.cad.ci 0.21.0` @
  `b1474f6be66dc0236f2a5c2555af07a100447255`.
- `lib.py.cad.ci 0.11.1` @
  `fa6bf244381dde609a0b04de673d774911c52fea`.
- Acceptance PR #87 was squashed to main @
  `8218effedfc25c70b76d4237c15d1ff7aa47b709`.
- Full released-stack run `45045346481` succeeded.

`dependencies.repos`, public reusable workflows, the advanced plan API, root
composite action, durable same-runner case and merge-policy checks all exercise
the exact released tool stack.

## Current work

No acceptance migration is active. Future tool/library releases must be pinned
here by exact immutable commit and pass the full suite before Forge/CAD adoption.

A failure belongs in the owning library/tool repository; do not patch around
generic behavior in this test repository.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #88 Align historical changelog with shared meta template and guidance | **later / docs-only** | Apply shared changelog presentation without changing acceptance behavior. |

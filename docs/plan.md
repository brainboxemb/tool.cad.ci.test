# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22). This repository is the permanent external black-box acceptance
repository and owns no CAD-CI algorithms.

## Accepted baseline

- currently accepted: `tool.cad.ci 0.21.0`;
- candidate under issue #90: `tool.cad.ci 0.22.0` @
  `76b5ba24084a09a69e6f25b34c16e869f7240a58`;
- `lib.py.cad.ci 0.11.1` remains @
  `fa6bf244381dde609a0b04de673d774911c52fea`.

## Current work

### #90 — accept tool.cad.ci 0.22.0

1. repin every existing public workflow/action acceptance case to 0.22.0;
2. keep the complete existing behavioral suite green;
3. verify released template manifest, ids/versions and public surface mapping;
4. verify released templates retain one immutable release marker and contain
   no copied generic implementation or existing consumer names;
5. merge only after green acceptance;
6. then Forge/CAD may migrate their wrappers from released templates.

A failure belongs in the owning tool/library repository; do not patch around
generic behavior here.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #90 Accept tool.cad.ci 0.22.0 consumer-template release | **now** | Full released-stack + template acceptance. |
| #88 Align historical changelog with shared meta template and guidance | **later / docs-only** | No behavior impact. |

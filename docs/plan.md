# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.19.0` @
  `5677c41a61929b32ab2cb07087a6505f7b9347d8`;
- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Acceptance #80 / PR #81 / run `45022699789` is complete.

Accepted public behavior includes:

- direct CLI and reusable workflow consumption;
- root same-runner action in run-only and durable long-lived-scope modes;
- jobs=2 bounded execution;
- dependency-output `copy:`;
- exact durable build publication and prepared-scope handoff;
- immediate same-runner post-action inspection without artifact transport;
- released shared merge-policy workflow for short-lived squash merges and
  configured lane-to-stable normal-merge promotion.

## Current work

Issue #82 — **now**: externally accept released `tool.cad.ci 0.20.0` at exact
commit `d45cdcef33cf1035311bab9a88c3f99208ef3b29`.

The release keeps the exact accepted `lib.py.cad.ci 0.11.0` pin and extends
only the tool-owned merge/lifecycle workflow with history-preserving
stable-to-configured-lane synchronization.

Acceptance order:

1. repin every released tool/workflow/action consumer to exact 0.20.0;
2. rerun the complete existing black-box suite;
3. validate the released helper distinguishes lane promotion, stable-to-lane
   synchronization and ordinary squash merges;
4. validate both permanent merge directions require same-repository source;
5. validate stable-to-lane synchronization leaves stable source lifecycle
   untouched while integrating the updated lane/base;
6. leave the real remote branch mutation to Forge #717 after this repository is
   green.

Do not add local merge-policy implementation here.

## Open issue assessment — 2026-11-22

| Issue | Status | Current interpretation |
| --- | --- | --- |
| #82 accept tool.cad.ci 0.20.0 stable-to-lane policy | **now** | Repin exact released tool, run full suite, validate both permanent merge directions; Forge #717 performs the real branch mutation afterward. |

## Boundary

Do not implement or patch generic CAD-CI behavior here.

If acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

## Recently completed

- #80 accepted tool.cad.ci 0.19.0 merge-policy workflow at exact
  `5677c41a...`; full acceptance run `45022699789` succeeded.

# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.20.0` @
  `d45cdcef33cf1035311bab9a88c3f99208ef3b29`;
- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Acceptance #82 / PR #83 / run `45031453651` is complete.

Accepted public behavior includes:

- direct CLI and reusable workflow consumption;
- root same-runner action in run-only and durable long-lived-scope modes;
- jobs=2 bounded execution;
- dependency-output `copy:`;
- exact durable build publication and prepared-scope handoff;
- immediate same-runner post-action inspection without artifact transport;
- shared merge policy with short-lived squash merges;
- configured lane-to-stable normal-merge promotion;
- configured stable-to-lane history-preserving normal-merge synchronization.

## Current work

Issue #84 — **now**: externally accept released `tool.cad.ci 0.20.1` at exact
commit `eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9`.

The release retains exact `lib.py.cad.ci 0.11.0` and fixes the merge-command
self-check deadlock exposed by Forge #721. Same-head Actions runs triggered by
`issue_comment` are command workflows, not PR validation checks.

Acceptance order:

1. repin every released tool/workflow/action consumer to exact 0.20.1;
2. rerun the complete existing black-box suite;
3. retain every 0.20.0 merge-classification/lifecycle check;
4. validate the released workflow queries same-head
   `event=issue_comment` Actions runs and filters matching check-runs by run
   identity before latest-check grouping;
5. validate the non-command validation set remains mandatory and normal
   failed/pending checks remain blocking;
6. leave the real same-head command execution proof to Forge #721 after this
   repository is green and Forge adopts the exact release.

Do not add local merge-policy implementation here.

## Open issue assessment — 2026-11-22

| Issue | Status | Current interpretation |
| --- | --- | --- |
| #84 accept tool.cad.ci 0.20.1 command-check isolation | **now** | Repin exact released tool, run full suite, verify command-check filtering contract; Forge performs the real stable-head merge command afterward. |

## Boundary

Do not implement or patch generic CAD-CI or merge-policy behavior here.

If acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

## Recently completed

- #82 accepted tool.cad.ci 0.20.0 stable-to-lane merge policy at exact
  `d45cdcef...`; full acceptance run `45031453651` succeeded.
- #80 accepted tool.cad.ci 0.19.0 merge-policy workflow at exact
  `5677c41a...`; full acceptance run `45022699789` succeeded.

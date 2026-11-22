# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.18.1` @
  `e29d3127d5d3f9310f3cab4e27430a64a61c21cc`;
- `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Acceptance #77 / PR #78 / run `45019713862` is complete.

Accepted public behavior includes:

- direct CLI and reusable workflow consumption;
- root same-runner action in run-only mode;
- root same-runner action in durable long-lived-scope mode;
- jobs=2 bounded execution;
- dependency-output `copy:`;
- exact durable build publication and prepared-scope handoff;
- immediate same-runner post-action inspection without artifact transport.

## Current work

Issue #80 — **now**: externally accept released tool.cad.ci 0.19.0 at exact
commit `5677c41a61929b32ab2cb07087a6505f7b9347d8`.

The release keeps the exact accepted lib.py.cad.ci 0.11.0 pin and adds only a
tool-owned reusable merge/lane-policy workflow surface.

Acceptance order:

1. repin every released tool/workflow/action consumer to exact 0.19.0;
2. rerun the complete existing black-box suite unchanged;
3. validate the exact released `scripts/merge_policy.py` decision contract;
4. validate the exact released `reusable-merge-policy.yml` is repository
   neutral, fail-closed and does not accept an arbitrary merge method;
5. leave the real successful GitHub merge/ref mutation to Forge #674 consumer
   equivalence, so this repository does not leave synthetic branches/PRs behind.

Do not add local merge-policy implementation here.

Accepted additional behavior includes:

- opt-in `selection_context: direct_dependents` on command steps;
- signature-safe/current/cache-safe active-dependent context;
- public step evidence schema 5 with `active_dependents`;
- unchanged direct CLI, reusable workflow, same-runner action and durable
  publication behavior.

## Open issue assessment — 2026-11-22

| Issue | Status | Current interpretation |
| --- | --- | --- |
| #80 accept tool.cad.ci 0.19.0 merge-policy workflow | **now** | Repin exact release, run full suite, validate released helper/workflow contract; real mutating success path is subsequent Forge #674 qualification. |

## Boundary

Do not implement or patch generic CAD-CI behavior here.

If future acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

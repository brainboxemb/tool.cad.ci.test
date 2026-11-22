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

No acceptance implementation is active.

The exact released 0.18.1 / 0.11.0 pair is externally accepted. Forge and CAD
may now adopt this pair through their own consumer plans.

Accepted additional behavior includes:

- opt-in `selection_context: direct_dependents` on command steps;
- signature-safe/current/cache-safe active-dependent context;
- public step evidence schema 5 with `active_dependents`;
- unchanged direct CLI, reusable workflow, same-runner action and durable
  publication behavior.

## Open issue assessment — 2026-11-22

No open acceptance issues remain after #77 is closed.

## Boundary

Do not implement or patch generic CAD-CI behavior here.

If future acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

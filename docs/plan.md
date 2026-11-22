# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.18.0` @
  `b62f9d0b169aa201a3c66c3166f364396b2d71bc`;
- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`.

Acceptance #73 / PR #74 / run `45010776155` is complete.

Accepted public behavior includes:

- direct CLI and reusable workflow consumption;
- root same-runner action in run-only mode;
- root same-runner action in durable long-lived-scope mode;
- jobs=2 bounded execution;
- dependency-output `copy:`;
- exact durable build publication and prepared-scope handoff;
- immediate same-runner post-action inspection without artifact transport.

## Current work

### #77 accept tool 0.18.1 / library 0.11.0

Status: **now**.

Exact released pair:

- `tool.cad.ci 0.18.1` @ `e29d3127d5d3f9310f3cab4e27430a64a61c21cc`;
- `lib.py.cad.ci 0.11.0` @ `e621daf6e309bdd0e3f643a12007f1b66490696d`.

Acceptance scope:

- repin direct CLI bootstrap, reusable workflow and same-runner action to the exact tool release;
- update exact expected library revision and public step-evidence schema to the released library contract;
- add one synthetic shared-producer/two-consumer case for `selection_context: direct_dependents`;
- prove consumer-a only, repeat/current, consumer-b only signature invalidation, both consumers with jobs=2, full run and public `active_dependents` evidence;
- add no generic implementation or domain-specific Forge/CAD behavior.

Forge/CAD adoption remains blocked until the complete PR acceptance suite is green.

## Open issue assessment — 2026-11-22

| Issue | Status | Next action |
| --- | --- | --- |
| #77 accept tool 0.18.1 / lib 0.11.0 | **now** | Repin exact released stack and prove active direct-dependent context end-to-end. |

## Boundary

Do not implement or patch generic CAD-CI behavior here.

If future acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

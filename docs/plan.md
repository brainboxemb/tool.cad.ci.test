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

No acceptance implementation is active.

A new acceptance issue starts only after a new exact released tool/library pair
or public action contract exists.

## Boundary

Do not implement or patch generic CAD-CI behavior here.

If future acceptance exposes a generic defect, return to the owning library/tool,
release the corrected stack, then repin the exact release here and rerun the
complete black-box suite.

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

Acceptance issue #73 / PR #74 is complete.

Complete released-stack run `45010776155` passed:

- direct released CLI cases;
- reusable workflow consumers;
- no-output reusable workflow behavior;
- jobs=2 bounded execution;
- dependency-output `copy:`;
- durable build and Pages publication;
- the root composite action in durable same-runner mode;
- immediate post-action inspection of the returned `prepared_scope` and exact
  generated build commit on that same runner.

No action artifact upload/download or second post-action runner is part of the
accepted durable contract.

Issue #73 is complete and closed.

## Current work

No acceptance implementation is active.

A new acceptance issue starts only after:

- a new exact released tool/library pair exists; or
- an already released public surface needs a new black-box consumer contract.

## Boundary

Do not implement or patch generic/tool behavior here.

If future acceptance exposes a generic defect:

1. return to `lib.py.cad.ci` when engine/build-store behavior is generic;
2. otherwise return to `tool.cad.ci` for CLI/workflow/action surface behavior;
3. publish the corrected owner release;
4. pin that exact released tool here;
5. rerun the complete black-box suite.

Consumers may adopt the accepted tool 0.18.0 / lib 0.10.0 pair.

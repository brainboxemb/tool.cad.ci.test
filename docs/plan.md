# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.17.0` @
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`.

Issue #66 / PR #67 passed the complete released-stack suite.

Accepted evidence includes:
- reusable workflow with jobs=2;
- same-runner composite action with jobs=2;
- direct released CLI jobs=2;
- overlapping public step-evidence action intervals proving bounded parallel
  SCons execution.

## Current work

### #70 — accept dependency-output copy on the exact released stack

New released stack under acceptance:

- `tool.cad.ci 0.17.1` @
  `1012e6a539a2fddd8194124844fe208bf16cf4e4`;
- pinned `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`.

The new generic capability is library-owned `copy:` for projecting declared
outputs from one direct dependency bundle without a consumer copy subprocess or
complete dependency-snapshot materialization.

Acceptance order:

1. pin only the exact released tool revision everywhere this repository consumes
   the stack;
2. update the expected exact library revision;
3. add one synthetic dependency-copy case using only public YAML/CLI/evidence;
4. prove cold BUILT output, `action_type=copy`, schema 4, null exit/timeout and
   CURRENT reuse;
5. keep every existing black-box case green;
6. keep reusable workflow and same-runner action paths green on the exact same
   released tool revision;
7. after green PR acceptance, record the accepted stack here and close #70;
8. only then may Forge #261 adopt projection-only copy steps.

## Open issue assessment — 2026-11-22

| Issue | Status | Assessment |
| --- | --- | --- |
| #70 Accept tool.cad.ci 0.17.1 / lib.py.cad.ci 0.10.0 dependency-output copy | **now** | Required exact released-stack black-box gate before Forge consumer migration. |

## Boundary

Do not implement or patch generic copy behavior here.

If this acceptance exposes a generic defect:
- return to `lib.py.cad.ci` #79;
- release a corrected library;
- repin/release the thin tool;
- restart acceptance from exact released commits.

After #70 completes, this repository returns to demand-driven acceptance mode.

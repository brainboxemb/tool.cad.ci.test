# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.17.1` @
  `1012e6a539a2fddd8194124844fe208bf16cf4e4`;
- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`.

Acceptance issue #70 / PR #71 is complete.

Complete released-stack run `45006989548` passed:

- direct released CLI cases;
- reusable high-level workflow;
- same-runner composite action;
- jobs=2 bounded parallelism;
- selective startup;
- durable publication;
- timeout/failure behavior on public step-evidence schema 4;
- dependency-output `copy:` with child-owned output bytes,
  `action_type=copy`, null exit/timeout and CURRENT reuse.

The dependency-copy case is synthetic and domain-neutral. No generic
implementation is stored in this repository.

## Current work

No acceptance implementation is active.

A new acceptance issue starts only after:

- a new exact released tool/library pair exists; or
- an already released public surface needs a new black-box consumer contract.

## Boundary

Do not patch generic behavior here.

If future acceptance exposes a generic defect:

1. return to `lib.py.cad.ci`;
2. release the corrected library;
3. repin/release `tool.cad.ci`;
4. pin that exact released tool here;
5. rerun the complete black-box suite.

Consumers may now adopt the accepted 0.17.1/0.10.0 pair.

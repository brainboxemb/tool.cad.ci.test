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

Issue #66 / PR #67 passed the complete exact released-stack suite.

Accepted evidence includes:
- reusable workflow with jobs=2;
- same-runner composite action with jobs=2;
- direct released CLI jobs=2;
- two independent public step-evidence action intervals overlapped:
  - left: 22:33:20.506Z -> 22:33:22.029Z;
  - right: 22:33:20.507Z -> 22:33:22.029Z.

The overlap is behavioral proof of actual bounded SCons parallel execution; no
fixed elapsed-time threshold was required.

## Current work

No acceptance implementation is active.

A new acceptance issue starts only after:
- a new exact released tool/library pair exists; or
- an already released public surface needs a new black-box consumer contract.

The repository must continue to pin exact released revisions, use only public
consumer surfaces, avoid implementation imports and keep the complete existing
suite green.

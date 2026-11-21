# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted stack

- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`;
- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`.

Issue #62 / PR #63 passed the complete released-stack suite, including:
- direct bootstrap;
- reusable workflow;
- same-runner action;
- normal selection/dependency/rerun/publication cases;
- selective-startup active-closure acceptance.

The selective-startup case observed a 0.446 s selected run. That value is
diagnostic evidence, not a performance threshold.

## Current work

No acceptance implementation is active.

A future acceptance issue starts only when an exact new released tool/library
pair exists or when a new released tool surface needs black-box proof.

This repository must continue to:
- pin exact released revisions;
- use only public consumer surfaces;
- avoid importing CAD-CI implementation internals;
- prove externally observable behavior rather than duplicating library tests;
- keep the complete existing suite green when adding new acceptance.

## Next known trigger

`tool.cad.ci` #76 may later expose the already released library `jobs`
option. If that work is released, this repository should create a fresh issue
that pins the new exact tool revision and proves `jobs > 1` through the public
tool surface before any consumer adopts it.

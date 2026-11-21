# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted baseline

Previously accepted:
- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`;
- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`.

Issue #62 / PR #63 proved the selective-startup optimization and the complete
released-stack suite.

## Current work

Issue #66 is **now**.

Candidate exact released stack:
- `tool.cad.ci 0.17.0` @
  `d88d6e189c12edb5a30158c068145c099c17a019`;
- pinned `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`.

Required black-box proof:
1. repin every producer entry point to exact tool 0.17.0;
2. exercise `jobs: 2` through reusable workflow and same-runner action;
3. use the released CLI on a synthetic repository with two independent targets;
4. prove actual parallel execution from public step evidence by overlapping
   `started_at` / `finished_at` action intervals;
5. keep default/legacy acceptance cases green;
6. use no CAD-CI implementation imports and no fixed wall-clock pass threshold.

## Gate

Forge may opt into `jobs > 1` only after #66 is accepted.

Default `jobs=1` remains the compatibility baseline; acceptance of `jobs=2`
proves the opt-in surface, not a new global default.

## Execution order

1. [#66] Exact 0.17.0 repin and jobs=2 surface proof.
2. [#66] Complete released-stack suite green.
3. Merge acceptance only after every public surface passes.
4. Forge may then open a separate dev-ci consumer experiment with one deliberate
   bounded jobs value and measure a full promotion.

# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests one exact released `tool.cad.ci` stack. It
must not contain generic CAD-CI implementation.

## Current status

The previous named-scope acceptance (#60) is complete.

Current released stack under acceptance:

- `lib.py.cad.ci 0.9.3` @
  `74486c441f1f2b170ff3dc06e0edcaf662fbec6b`;
- `tool.cad.ci 0.16.2` @
  `59e4c4d3f377f906b33bb2d1fee808f96c6fb1b9`.

The library release changes only generic selective SCons manifest preparation:
active target closure is resolved before source inputs and one source inventory
is shared across active steps.

## Current goal

Complete #62 against exact released tool.cad.ci 0.16.2.

The new black-box case must prove the active-closure behavior through public CLI
results, without importing CAD-CI internals and without a fragile wall-clock
threshold.

## Required proof

- direct bootstrap pins exact tool 0.16.2;
- reusable workflow and same-runner action use that same exact commit;
- expected library revision is exact lib.py.cad.ci 0.9.3;
- a selected item plus dependency succeeds even when an unrelated processed
  item has a configured input matching a symlink;
- selecting that symlink-owning item still fails with the documented safety
  error;
- the complete existing black-box suite remains green.

## Execution order

1. [#62, now] Repin all released-stack entry points.
2. [#62] Add the selective-startup consumer case.
3. [#62] Run the complete pull-request acceptance suite.
4. Merge only when every exact released-stack path is green.
5. [Forge] Adopt tool 0.16.2 / lib 0.9.3 and remeasure the real selective PR
   startup interval.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #62 Accept released selective-startup optimization | **now** | Exact released stack exists; prove active-closure behavior and retain complete-suite compatibility. |

Immediate chain:

`acceptance #62 -> Forge adoption/measurement`.

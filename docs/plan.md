# Repository plan

This file is the current source of truth for unfinished work in
`tool.cad.ci.test`.

The repository externally tests exact released `tool.cad.ci` /
`lib.py.cad.ci` pairs. It must not contain generic CAD-CI implementation.

## Current accepted baseline

- `tool.cad.ci 0.17.1` @
  `1012e6a539a2fddd8194124844fe208bf16cf4e4`;
- `lib.py.cad.ci 0.10.0` @
  `397fb04005b46de8d433cb18c091b1e73714b877`.

Acceptance #70 / PR #71 / run `45006989548` is complete and covers the
existing CLI, reusable workflow, same-runner run-only action, jobs=2, durable
publication, dependency-output copy and the full black-box suite.

## Current work

### #73 — accept tool.cad.ci 0.18.0 durable same-runner action

Status: **now**.

Released candidate:

- `tool.cad.ci 0.18.0` @
  `b62f9d0b169aa201a3c66c3166f364396b2d71bc`;
- exact pinned `lib.py.cad.ci 0.10.0` remains
  `397fb04005b46de8d433cb18c091b1e73714b877`.

The new public capability extends the existing root composite action with
optional durable-lane orchestration. It deliberately keeps one caller runner
and one CAD-CI/SCons graph.

Acceptance sequence:

1. pin the exact released 0.18.0 tool commit everywhere;
2. keep the complete existing suite green;
3. convert the existing `same_runner` acceptance job to durable mode rather
   than adding another runner/job;
4. use a fixed named scope `durable-action-acceptance`;
5. prove the action returns exact scope/base/full-run/build-commit/prepared
   scope outputs;
6. in the immediately following step of that same job, inspect the prepared
   scope directly from the same workspace;
7. fetch/inspect the exact returned generated-build commit and prove its named
   scope build manifest records the same source SHA;
8. prove the exact tool/library stack remains importable after the action;
9. use no action artifact upload/download or second post-action job.

Only after this exact released action passes may Forge remove its duplicated
durable scope/base/build-publication shell.

## Open issue assessment — 2026-11-22

| Issue | Status | Assessment |
| --- | --- | --- |
| #73 Accept tool.cad.ci 0.18.0 same-runner durable lane action | **now** | Required released-surface gate before Forge workflow simplification. |

## Boundary

Do not implement or patch durable behavior here.

If acceptance exposes a tool-surface defect:

1. return to `tool.cad.ci` #95;
2. publish a corrected tool release;
3. repin the exact release here;
4. rerun the complete black-box suite.

If it exposes a generic engine/build-store defect, return to `lib.py.cad.ci`
first.

After #73 completes, this repository returns to demand-driven acceptance mode.

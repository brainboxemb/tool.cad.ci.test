# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- accepted under #133 / PR #135: `tool.cad.ci v0.25.0` @
  `92b9cbb59bf24f6b47ba1fae267f67f2becc503f`;
- v0.25.0 pins `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- v0.25/main + numbered dev-ci histories were reconciled by PR #140;
- numbered standalone test roots `001` through `012` are present on
  `dev-ci`;
- declarative builder migrations accepted on `dev-ci`:
  - `001_simple` — PR #143;
  - `002_selection` — PR #145;
  - `003_fresh_runner` — PR #147;
  - `004_nested_items` — PR #149;
  - `005_nested_publish` — PR #151;
  - `006_dependencies` — PR #153;
  - `007_dependency_copy` — PR #161;
- acceptance timing observability landed in PR #159.

## Current work

### #142 — migrate numbered roots to declarative builders

Use `test_roots/011_shared_builder` as the canonical builder-model reference.

Normal executable item `ci.yml` files should contain item identity,
`builder:`, selection/watch/dependency/process configuration, but not
executable `steps:` / `run:`.

`008_active_dependents` is migrated and accepted on `dev-ci` by PR #165.

`009_partial_rerun` is the next migration and requires an explicit design
check because its public contract selects named builder steps with
`--step` / `--until` / `--from`.

### #156 — acceptance case duration and suite performance

Per-case timing and machine-readable evidence landed in PR #159.

Accepted total case-time baselines now include:

- 17.341 s — post-merge dev-ci run `45068161840`;
- 21.135 s — post-promotion main run `45068580019`;
- 23.996 s — simultaneous post-promotion dev-ci run `45068582403`;
- 24.294 s — PR #159 run `45067237488`;
- 24.842 s — accepted follow-up run `45067522266`;
- 25.444 s — lane-promotion PR run `45068453493`.

Initial non-failing soft budgets are therefore:

- total suite: 30 s;
- default case: 3 s;
- timeout case: 4 s;
- publish case: 7 s.

Warnings are observability only; no timing threshold fails acceptance.

### #114 — normalize remaining external cases into numbered test roots

#114 owns only the remaining historical top-level fixture audit/migration after
the existing numbered roots prove the builder architecture.

Do not mechanically migrate special workflow/governance harness cases.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using
`reusable-ci.yml@v0.25.0` and the released lane/merge policy.

### #106 — prove dev-cad to main promotion

Complete the real promotion proof after the docs-only lane change. Keep this as
integration evidence; do not add another acceptance execution route or
duplicate generic merge/classification logic.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #142 Declarative builder migration | **now** | `001`–`008` accepted; design/migrate `009_partial_rerun` next. |
| #156 Acceptance duration | **now** | Land conservative non-failing soft warnings from the accepted timing baseline. |
| #114 Numbered standalone test roots | **blocked by #142 for normal roots** | Resume remaining top-level fixture migration after builder migration. |
| #106 dev-cad -> main promotion proof | **active integration** | Finish the real promotion scenario and record lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy, builder resolution and CAD-CI behavior
remain in the released tool/library stack.

Do not migrate Forge/CAD consumers to the builder model until this repository
proves the model across its existing numbered use cases.

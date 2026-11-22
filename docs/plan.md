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
- acceptance timing observability landed in PR #159.

## Current work

### #142 — migrate numbered roots to declarative builders

Use `test_roots/011_shared_builder` as the canonical builder-model reference.

Normal executable item `ci.yml` files should contain item identity,
`builder:`, selection/watch/dependency/process configuration, but not
executable `steps:` / `run:`.

`007_dependency_copy` is the current migration under #155. Its engine-native
`copy:` action moves into a shared repository-owned builder; consumer item
configs retain only identity, builder selection and dependency declaration.

After `007`, continue existing numbered roots in order. `009_partial_rerun`
still requires an explicit design check because its public contract selects
builder steps.

### #156 — acceptance case duration and suite performance

Per-case timing and machine-readable evidence landed in PR #159.

First measured baseline from run `45067237488`:

- total measured case time: 24.294 s across 18 cases;
- `publish_case`: 5.867 s;
- `timeout_case`: 2.946 s;
- `006_dependencies`: 1.823 s;
- `012_parallel_jobs`: 1.752 s;
- `009_partial_rerun`: 1.576 s;
- `008_active_dependents`: 1.416 s.

Keep #156 open while subsequent accepted runs establish enough evidence for
soft performance budgets. Do not introduce hard thresholds from a single run.

### #154 — formalize live GitHub workflow scenarios

Keep synthetic consumer-root acceptance separate from live GitHub lifecycle
acceptance. Maintain explicit real scenarios for feature PRs, docs-only PRs,
lane promotion, stable-to-lane synchronization and owner `/merge` comments.

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
| #142 Declarative builder migration | **now** | Qualify `007_dependency_copy`, then continue existing roots in order. |
| #156 Acceptance duration | **active measurement** | Collect timings from subsequent real acceptance runs; derive soft budgets later. |
| #154 Live GitHub workflow scenarios | **active** | Maintain real PR/lane/merge workflow acceptance separately from test roots. |
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

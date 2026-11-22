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

`009_partial_rerun` is migrated and accepted on `dev-ci` by PR #177.

`010_process` is migrated and accepted on `dev-ci` by PR #179.

`011_shared_builder` is already the canonical shared-builder reference.

`012_parallel_jobs` is the current and final existing numbered-root migration
under #182. Both items share one repository-owned builder while the public
`--jobs 2` overlap contract remains unchanged.

Acceptance timing is now part of the accepted baseline: PR #159 added
per-case evidence and PR #175 added conservative non-failing soft budgets.
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
| #142 Declarative builder migration | **now** | `001`–`011` accepted/canonical; qualify final existing root `012_parallel_jobs` under #182, then audit all item configs. |
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

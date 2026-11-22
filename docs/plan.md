# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- accepted under #133 / PR #135: `tool.cad.ci v0.25.0` @
  `92b9cbb59bf24f6b47ba1fae267f67f2becc503f`;
- v0.25.0 pins `lib.py.cad.ci 0.12.0` @
  `64656db8df528a5c0de799e62c0f028fd0133486`;
- released-stack acceptance run #176 (`45063532187`) passed,
  including `test_roots/011_shared_builder`;
- v0.25/main + numbered dev-ci histories were reconciled by PR #140;
- config-driven acceptance architecture passed in PR #94;
- case ownership/documentation cleanup passed in PR #97;
- numbered standalone test roots `001` through `012` are present on
  `dev-ci`.

## Current work

### #156 — acceptance case duration and suite performance

Measure every registered case centrally, print a slowest-first summary and
retain machine-readable timing evidence. Use real accepted runs to establish a
baseline before introducing any hard performance budget.


### #142 — migrate numbered roots to declarative builders

Use `test_roots/011_shared_builder` as the canonical builder-model reference.

Normal executable item `ci.yml` files should contain item identity,
`builder:`, selection/watch/dependency/process configuration, but not
executable `steps:` / `run:`.

Migrate the already-numbered roots before adding more normal test roots.
`001_simple` is migrated and accepted on `dev-ci` by PR #143.
`002_selection` is migrated and accepted on `dev-ci` by PR #145.
`003_fresh_runner` is migrated and accepted on `dev-ci` by PR #147.
`004_nested_items` is migrated and accepted on `dev-ci` by PR #149.
`005_nested_publish` is migrated and accepted on `dev-ci` by PR #151.
`006_dependencies` is the current migration under #152; producer, shared
consumer and summary execution move into repository-owned builders while
public dependency flow and step names stay unchanged.

`007_dependency_copy` and `009_partial_rerun` require explicit design checks
because their public contracts involve copy/step-selection semantics.

### #114 — normalize remaining external cases into numbered test roots

Keep this separate from #142. #114 owns only the remaining historical top-level
fixture audit/migration after the existing numbered roots prove the builder
architecture.

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
| #142 Declarative builder migration | **now** | `001`–`005` complete; qualify `006_dependencies`, then continue in order. |
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

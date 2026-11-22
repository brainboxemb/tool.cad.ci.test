# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Accepted baseline

- `tool.cad.ci v0.24.0` @
  `18d374fad83e61b9a9b057931352ce4a2c8e2252`;
- `lib.py.cad.ci 0.11.1` @
  `fa6bf244381dde609a0b04de673d774911c52fea`;
- v0.24.0 external acceptance passed in #102 / PR #104;
- config-driven acceptance architecture passed in PR #94;
- case ownership/documentation cleanup passed in PR #97.

## Current work

### #111 — establish test_roots/001_simple

Replace the historical `simple_case1` fixture with the first numbered,
self-contained consumer repository:

```text
test_roots/001_simple/
  README.md
  cad-ci.yml
  ci.yml
  hello.md
  build.py
  check.py
```

It proves only cold build, current rerun and rebuild after changing
`hello.md`. Future standalone acceptance repositories follow the same
three-digit `test_roots/NNN_name` convention.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using
`reusable-ci.yml@v0.24.0` and the released lane/merge policy.

### #106 — prove dev-cad to main promotion

Complete the current real promotion proof after the docs-only lane change.
Keep this as integration evidence; do not add another acceptance execution
route or duplicate generic merge/classification logic.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #111 Numbered standalone test roots | **now** | Land and prove `test_roots/001_simple`. |
| #106 dev-cad -> main promotion proof | **active integration** | Finish the real promotion scenario and record resulting lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack. Every retained acceptance case stays locally documented and
must prove a distinct public contract.

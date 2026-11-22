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
- case ownership/documentation cleanup passed in PR #97;
- numbered standalone test roots established:
  - `001_simple`;
  - `002_selection`;
  - `003_fresh_runner`;
  - `004_nested_items` in #119.

## Current work

### #114 — normalize remaining external cases into numbered test roots

Audit each historical top-level case before migration. Retain only distinct
public consumer contracts, remove owner-level/obsolete duplicates, and place
retained standalone repositories below `test_roots/NNN_name/`.

After `004_nested_items`, nested durable publication remains a separate next
candidate; it must not be merged into nested discovery/selection.

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
| #119 `004_nested_items` | **now** | Land/prove the fourth standalone test root. |
| #114 Numbered standalone test roots | **active umbrella** | Audit/migrate the next distinct consumer use case. |
| #106 dev-cad -> main promotion proof | **active integration** | Finish the real promotion scenario and record resulting lane evidence. |
| #98 Permanent lane integration | **active umbrella** | Continue canonical synchronization/promotion scenarios. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack. Every retained acceptance case stays locally documented and
must prove a distinct public contract.

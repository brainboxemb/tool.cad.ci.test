# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Baseline

- accepted baseline: `tool.cad.ci v0.23.0`;
- candidate under external acceptance: `tool.cad.ci v0.24.0` @
  `18d374fad83e61b9a9b057931352ce4a2c8e2252`;
- both pin `lib.py.cad.ci 0.11.1`;
- config-driven external acceptance passed in PR #94;
- case ownership/documentation cleanup passed in PR #97.

## Current work

### #102 — accept tool.cad.ci v0.24.0

1. repin the single normal `reusable-ci.yml` consumer path to `v0.24.0`;
2. retain the canonical permanent-lane policy introduced by #98/#99;
3. update release-identity assertions only;
4. run the complete current acceptance suite;
5. do not add root-action/same-runner or alternate execution routes;
6. mark v0.24.0 accepted only after the complete suite is green.

### #98 — permanent lane integration

Continue exercising the real external permanent-lane contract on
`main`, `dev-cad` and `dev-ci` using the released lane policy and merge
workflow. The v0.24.0 repin must not undo that integration topology.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #102 Accept tool.cad.ci v0.24.0 | **now** | Merge after complete external acceptance is green. |
| #98 Permanent lane integration | **active** | Continue real lane PR/promotion/synchronization scenarios after the release repin. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack.

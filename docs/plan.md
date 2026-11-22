# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Baseline

- accepted baseline: `tool.cad.ci v0.23.0`;
- `v0.23.0` pins `lib.py.cad.ci 0.11.1`;
- config-driven external acceptance passed in PR #94;
- case ownership/documentation cleanup passed in PR #97.

## Current work

### #98 — establish permanent lane integration

Make this repository the real external consumer of the standard permanent-lane
contract:

1. maintain permanent `main`, `dev-cad` and `dev-ci` branches;
2. use released `reusable-ci.yml@v0.23.0` with canonical lane PR policy;
3. keep one normal workflow route only;
4. use released merge-policy for history-preserving lane promotion and
   synchronization;
5. dispatch the same `ci.yml` for complete post-merge integration validation;
6. prove issue/feature -> lane, docs-only lane PR, lane -> main promotion and
   main -> lane synchronization with real GitHub PRs;
7. keep `delete_branch_on_merge=false` and merge commits enabled.

Repository settings were verified before integration work:
`delete_branch_on_merge=false`, `allow_merge_commit=true`.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #98 Permanent lane integration | **now** | Land consumer wrappers on dev-ci, then exercise real lane PR paths. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns external acceptance/integration evidence only. Generic
lane classification, merge policy and CAD-CI behavior remain in the released
tool/library stack.

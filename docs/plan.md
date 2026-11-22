# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22).

## Baseline

- accepted baseline: `tool.cad.ci v0.22.0`;
- candidate: `tool.cad.ci v0.23.0`;
- the candidate pins `lib.py.cad.ci 0.11.1`.

## Current work

### #93 — simplify external acceptance architecture

Make this repository a normal config-driven consumer:

1. one `reusable-ci.yml@v0.23.0` GitHub workflow call;
2. one root `cad-ci.yml`;
3. one configured acceptance-suite item;
4. use the tool/library stack already loaded by the reusable workflow;
5. remove bootstrap/install duplication and root-action acceptance;
6. retain distinct black-box cases only for observable public behavior;
7. keep merge governance explicitly separate;
8. merge only after the complete simplified suite is green.

### #92 — accept v0.23.0 canonical lane consumers

The release-acceptance goal is folded into #93. Its previous requirement to
retain root-action acceptance is obsolete because `tool.cad.ci` #126 removes
that second public route. Close #92 when #93 proves v0.23.0.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #93 Simplify acceptance repository | **now** | Finish config-driven suite and prove v0.23.0. |
| #92 Accept v0.23.0 canonical lane consumers | **superseded by #93** | Close after #93 green/merged. |
| #88 Align historical changelog | **later / docs-only** | No runtime impact. |

## Boundary

This repository owns acceptance evidence only. Generic CI behavior belongs in
the released library/tool stack.

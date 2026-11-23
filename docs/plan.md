# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.31.0` @
  `27bdf67077ddd485cea95ba199069249c20c2a46`;
- v0.31.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- numbered standalone test roots `001` through `016` are accepted;
- normal CI, durable publication, permanent-branch governance, exact-SHA
  retirement and conservative cleanup have live GitHub evidence;
- durable live publication remains isolated on:
  - `test-output/build`;
  - `test-output/gh-pages`.

## Current work

### #232 — accept v0.32.0 post-build Pages renderer

**Now.** Exact `tool.cad.ci v0.32.0` is released at
`19e894567ac534ce90428dc61c6afa126c1d3318` and pins exact
`lib.py.cad.ci 0.15.0` @
`24c3abb267feea9ae91f24f8fdb435cba68f089a`.

The repository root must exercise the new library-owned
`publication.pages.builder/output` contract through the real released
`reusable-durable.yml` workflow. This is live GitHub acceptance; do not
replace it with library imports, a local durable workflow or a synthetic CLI
case.

Required order:

1. pin CI/governance wrappers to exact `v0.32.0`;
2. switch root Pages publication from the acceptance-suite item output to one
   repository-owned one-shot Pages builder;
3. remove the old site output from the normal acceptance-suite item so the
   live durable run cannot silently fall back to item/output mode;
4. require the existing full black-box suite green on the adoption PR;
5. merge the short-lived branch to `dev-ci` and require the real durable
   run green;
6. inspect reserved `test-output/build` and
   `test-output/gh-pages/dev-ci` to prove:
   - exact source SHA/ref;
   - exact generated build commit;
   - complete-scope manifest evidence;
   - repository variable precedence;
   - generic `provenance.json` agrees with builder-rendered context;
7. promote `dev-ci -> main`; require stable root Pages rendered through the
   post-build builder while preserving the named `dev-ci/` subtree;
8. synchronize `main -> dev-cad` and require its named durable publication
   green;
9. record v0.32.0 as fully accepted, then unblock Forge #740.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #232 Accept v0.32.0 post-build Pages renderer | **now** | Adopt exact release, prove live builder context and stable/named preservation. |

## Publication boundary

Normal `build` and `gh-pages` refs remain out of bounds for acceptance.
Live generated output stays on:

```text
test-output/build
test-output/gh-pages
```

The acceptance Pages builder is synthetic and repository-owned. It may read the
CAD-CI-owned publication environment and the materialized complete scope; it
must not import library internals, mutate generated refs, start another CAD-CI
graph or implement Pages branch logic.

## Existing evidence retained

- #141 / PR #216: durable workflow on reserved generated refs;
- #223 / PRs #225-#231: v0.31 public workflow names, promotion/sync,
  governance, exact-SHA retirement and cleanup;
- final v0.31 permanent refs are synchronized and no temporary issue branch
  remains.

## Boundary

This repository owns external acceptance evidence only. Generic builder
resolution, post-build renderer execution, provenance and Pages publication
remain in the released library/tool stack.

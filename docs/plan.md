# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- adopted repository wrappers: `tool.cad.ci v0.34.2` @
  `37f7a82c6769279d33367144c56976da89bb1a5d`;
- exact pinned `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- #248 completed CadQuery Workplane + Assembly acceptance and permanent-branch
  build publication;
- #254 separately completed real v0.35.0 targeted read-only selection
  acceptance; that focused scenario did not change the adopted repository
  wrappers;
- live generated output stays isolated on `test-output/*`.

## Candidate stack under acceptance

### #256 — accept v0.36.0 central CAD release flow

**Now.**

Candidate released stack:

- `tool.cad.ci v0.36.0` @
  `093eafb0eabf6b6617ec82dde17a76fdc718ae12`;
- exact pinned `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- the CAD release workflow delegates the GitHub release transaction to released
  `tool.py.lib.ci v0.2.1` @
  `58ead6897a4ac8cafef22a3c1f834491bf61568d`.

Required live sequence:

1. repin the consumer CI/governance wrappers to exact `v0.36.0` and add the
   copy-ready CAD release wrapper using `test-output/build`;
2. require the adoption PR to `dev-ci` green;
3. merge the short-lived branch to `dev-ci` and require the named dev-ci build
   green;
4. merge exact `dev-ci -> main` and require the main build to write
   `test-output/build/main/build.json` for the exact resulting main SHA;
5. comment `/release v0.36.0 <older-main-sha>` and require the CAD release
   build check to fail with no tag/release;
6. comment `/release v0.36.0 <exact-current-main-sha>` and require the build
   check plus delegated release transaction green;
7. verify the GitHub release/tag resolves to that exact main SHA;
8. repeat the exact successful command and require idempotent success;
9. record run IDs and SHAs on #256, then sync accepted `main -> dev-cad`.

Pages is not release evidence. The release scenario must not inspect
`test-output/gh-pages` or normal `gh-pages` when deciding release readiness.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #256 v0.36.0 central CAD release flow | **now** | Complete real issue-comment refusal, success and idempotency acceptance. |
| #253 selectable acceptance roots | **later** | Replace the monolithic acceptance-suite item separately; do not mix into #256. |

## Boundary

This repository owns external acceptance evidence only.

Do not add Forge/SolidCraft semantics, library imports, local release parsing,
build-record parsing, workflow bootstrap copies or a second CAD-CI graph.
Generic failures return to their owner repositories.

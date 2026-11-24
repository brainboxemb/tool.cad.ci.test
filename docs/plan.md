# Repository plan

This file contains unfinished work only.

## Now

### #263 — distinguish merge integration from manual dispatch

Live #261 acceptance proved the PR route, then exposed one event-routing gap:
the shared merge policy dispatches `ci.yml` after a GITHUB_TOKEN merge, so
the resulting permanent-branch integration arrives as `workflow_dispatch`
from `github-actions[bot]`.

Exact failing-routing evidence:

- dev-ci commit: `1e5d7000cf69bcc11962f43b145ba700cf1555ca`;
- integration run: `45364444766`;
- `manual_run` selected;
- `branch_build` skipped.

Route that bot dispatch to `branch_build` while keeping human manual dispatch
read-only. Then resume #261 live acceptance.

### #261 — Change 0001 reference consumer

Make this repository the living normal-consumer reference defined by
`tool.cad.ci` Change 0001.

Use exact released `tool.cad.ci v0.36.1` first; do not require a new tool
release when existing public workflows already provide the needed behavior.

Required behavior:

```text
pull request
  -> build / test / verify
  -> publish nothing

push main/dev-cad/dev-ci
  -> build / test / verify
  -> publish test-output branch build + Pages

manual
  -> full | item | changed_paths
  -> build / test / verify
  -> publish nothing
```

Required live proof:

1. PR validation on the issue branch;
2. merge to `dev-ci` and successful branch publication;
3. manual full read-only run;
4. manual exact-item read-only run;
5. manual changed-path read-only run;
6. confirm none of the manual runs updates `test-output/build` or
   `test-output/gh-pages`.

After that, the same structure can be copied back into the tool consumer manual
and adopted by Forge/product CAD.

## Later

### #253 — selectable acceptance roots

Break the monolithic acceptance-suite execution boundary into selectable
CAD-CI items after the reference consumer route is stable.

Do not mix this performance/organization change into #261.

## Boundary

This repository owns acceptance evidence, not generic CAD-CI implementation.

Generic failures return to `lib.py.cad.ci` or `tool.cad.ci`.

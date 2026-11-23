# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.31.0` @
  `27bdf67077ddd485cea95ba199069249c20c2a46`;
- v0.31.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- numbered standalone test roots `001` through `016` are accepted;
- normal CI, durable publication, merge governance, permanent-branch
  promotion/synchronization, conservative cleanup, exact-SHA retirement and
  reviewed conflict recovery have live GitHub evidence;
- durable live publication remains isolated on:
  - `test-output/build`;
  - `test-output/gh-pages`;
- the repository's normal `build` and `gh-pages` refs were not used for
  v0.31 acceptance.

## v0.31 public workflow-name acceptance

Completed issue #223 proves the renamed public workflow contract end to end.

Key evidence:

- PR #225 final black-box run #280 (`45147169700`) passed with
  `reusable-ci.yml@v0.31.0`, `pull_request_policy` and
  `command_environment`;
- bootstrap merge to `dev-ci` landed at
  `0b462f73a6921f9428a6ff268f5a9e6805e9cfa5`;
- dev-ci durable run #281 (`45147411390`) passed on reserved
  `test-output/*` generated refs;
- governance correction PR #226 run #282 (`45147615639`) passed, followed by
  corrected dev-ci durable run #283 (`45147791924`);
- promotion PR #227 run #284 (`45148007487`) classified the direct
  `dev-ci -> main` PR as `lane-promotion` and forced
  `POLICY_FULL_RUN=true`;
- history-preserving promotion merge
  `7fc5b28a3f72d1df6ed210fa8f48803fb619daa9` advanced both `main`
  and `dev-ci`;
- post-promotion durable runs #285 and #286 passed;
- PR #228 proved the v0.31 default-branch merge-policy itself:
  run #56 (`45148617436`) accepted `stable_branch`,
  `development_branches` and `permanent_branches`, then synchronized
  `main -> dev-cad` at
  `afaee0bf131145ecd3ee8a40de27ffa306da3384`;
- dev-cad durable run #288 (`45148658892`) passed;
- exact-SHA retirement run #44 (`45148940131`) removed superseded
  `issue/222-v0.31-workflow-names`;
- conservative cleanup run #49 (`45149155623`) removed the accidental empty
  `issue/219-v0.31-public-workflow-names` ref while preserving every
  permanent/generated ref.

Accepted public caller names are:

```text
stable_branch
development_branches
permanent_branches
temporary_branch_prefixes
resolution_branch_prefix
pull_request_policy
command_environment
```

JSON remains only the encoded value format for structured/list values. The
accepted consumer workflows do not expose the old `*_json` or
`lane_refs` names.

## Current work

No open acceptance/runtime issue.

## Existing governance evidence

- #180 / run `45070007017`: conservative branch cleanup;
- #186 / run `45071078228`: reviewed exact-SHA retirement;
- #200 / #203 / run `45075920227`: reviewed conflicted permanent sync recovery;
- #204 and merge `1e42ddb183c6e834b07e755862a165e891ec6cd6`:
  permanent-branch promotion full-run proof;
- #205/#206 and merge `a9406197e2f6cddfc0b1780b919d948ba3d7c16b`:
  reviewed main -> dev-ci conflict recovery;
- #207 promotion and runs `45132525063` / `45132528589`;
- #208 main -> dev-cad synchronization and run `45132783513`;
- #141 / PR #216: durable publication on reserved generated refs;
- #223 / PRs #225-#228: v0.31 public workflow-name and governance acceptance.

## Boundary

This repository owns external acceptance/integration evidence only. Generic
classification, merge policy, builder resolution and CAD-CI behavior remain in
the released tool/library stack.

Forge/CAD may consume the fully accepted v0.31.0 workflow contract; their own
repository migrations remain separately reviewed consumer work.

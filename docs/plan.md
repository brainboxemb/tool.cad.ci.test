# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.30.0` @
  `5fcd77d5a07a68ef97cfcdb52b534f85bec1f1f2`;
- v0.30.0 pins `lib.py.cad.ci 0.14.0` @
  `b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`;
- numbered standalone test roots `001` through `016` are accepted;
- merge governance, permanent-branch promotion/synchronization, conservative
  cleanup, exact-SHA retirement and reviewed conflict recovery have live GitHub
  evidence;
- the config-driven durable workflow is accepted end to end through completed
  issue #141, including isolated `test-output/*` generated refs.

## Current work

### #223 — accept v0.31.0 public workflow names

**Now.** Exact `tool.cad.ci v0.31.0` is released at
`27bdf67077ddd485cea95ba199069249c20c2a46` and still pins released
`lib.py.cad.ci 0.14.0` @
`b24e9a3826dfc07e07b4f3fd9971fcb4ab5aa12d`.

Adopt the renamed public workflow configuration without changing accepted
runtime behavior:

```text
stable_branch
development_branches
permanent_branches
temporary_branch_prefixes
resolution_branch_prefix
pull_request_policy
command_environment
```

Execution order:

1. update the real consumer workflows to v0.31.0 and the new public names;
2. run the complete black-box suite on PR #223's issue branch;
3. merge the short-lived issue branch to `dev-ci` through released v0.31
   merge governance;
4. prove durable `dev-ci` publication still uses only
   `test-output/build` and `test-output/gh-pages`;
5. promote `dev-ci -> main` through released v0.31 merge governance and
   confirm the permanent-branch lifecycle;
6. exercise v0.31 conservative cleanup against the accidental empty
   `issue/219-v0.31-public-workflow-names` ref;
7. record the accepted baseline and close #223.

Do not add aliases for v0.30 public names. Exact older release tags already own
that compatibility.

## Open issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #223 Accept v0.31.0 public workflow names | **now** | Adopt exact v0.31 workflows, run black-box PR, then prove governance on real refs. |

## Durable workflow evidence retained from #141

Reserved live acceptance output remains on:

```text
test-output/build
test-output/gh-pages
```

The repository's normal `build` and `gh-pages` refs are not acceptance
targets. #141 already proved stable/named scope and Pages preservation semantics;
#223 must preserve that behavior while changing only the public workflow names.

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
- #141 / PR #216: v0.30 durable publication on reserved generated refs.

## Boundary

This repository owns external acceptance/integration evidence only. Generic
classification, merge policy, builder resolution and CAD-CI behavior remain in
the released tool/library stack.

Forge/CAD remain on the fully accepted v0.30.0 baseline until #223 accepts
v0.31.0.

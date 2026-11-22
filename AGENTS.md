# Repository instructions

## Purpose

`tool.cad.ci.test` is the permanent external black-box acceptance repository
for one released `tool.cad.ci` + `lib.py.cad.ci` stack.

Keep it synthetic and domain-neutral. Do not add Forge, SolidCraft or real CAD
behavior.

## Consumer architecture

This repository must look like a normal consumer:

```text
one GitHub reusable workflow call
  -> one root cad-ci.yml
       -> configured acceptance suite
```

Do not add a second public execution route, root composite-action path,
plan/run workflow matrix, local bootstrap/install copy or manual list of test
commands in GitHub Actions.

The reusable workflow release tag is the consumer release identity. The loaded
tool itself pins the exact library revision.

## Permanent lanes

`main`, `dev-cad` and `dev-ci` are permanent branches.

- normal short-lived issue/feature PRs may target a development lane and are
  squash-merged;
- direct lane -> `main` promotion and `main` -> lane synchronization preserve
  history with merge commits;
- never rely on automatic merged-branch deletion for permanent lanes;
- consume the released lane classifier/merge policy; do not implement local
  branch-policy logic.

Repository settings must keep merge commits enabled and
`delete_branch_on_merge=false`.

## Black-box boundary

Acceptance cases may invoke the public `cad_ci_tool` CLI through subprocesses.
They must not import library planner, SCons, cache, build-store or publication
internals to reproduce decisions.

`tests/support.py` may provide only small process/file helpers and the path of
the already loaded released tool source.

If acceptance finds a generic gap, return to the owning library/tool repository.
Do not add a local workaround.

## Case organization

Standalone synthetic consumer repositories live under:

```text
test_roots/
  001_name/
  002_name/
  ...
```

Use three-digit numeric prefixes. Every test root owns its own root
`cad-ci.yml`; do not make the acceptance-repository root configuration stand
in for a test root's configuration.

Distinct synthetic repositories may remain only when they prove genuinely
different public behavior. GitHub Actions must not enumerate them individually;
the configured `acceptance_suite` owns that sequence.

Every registered case root must have a local `README.md` with:

- `Status:`;
- purpose;
- public contract;
- fixture/method;
- failure ownership.

Use `Status: current` for normal external acceptance. Mark owner-level or
temporary cases explicitly as transitional/separate API. An obsolete case must
not remain registered in `acceptance_suite/run.py`; remove it from execution
and then remove its fixture when no historical migration dependency remains.

Source-text assertions that merely freeze private workflow implementation are
not acceptance. Prefer observable public behavior.

Merge governance is a separately identified public API and may keep its own
black-box case while that API exists.

## Publication

Generated build/Page publication acceptance must use an isolated local Git
remote. Never write generated branches to this repository merely for testing.

## Development process

One logical change uses one issue, one branch and one pull request.

`docs/plan.md` is the current unfinished-work source of truth. Keep mutable
release/issue state there rather than in stable requirements/design text.

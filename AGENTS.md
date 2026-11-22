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

## Black-box boundary

Acceptance cases may invoke the public `cad_ci_tool` CLI through subprocesses.
They must not import library planner, SCons, cache, build-store or publication
internals to reproduce decisions.

`tests/support.py` may provide only small process/file helpers and the path of
the already loaded released tool source.

If acceptance finds a generic gap, return to the owning library/tool repository.
Do not add a local workaround.

## Case organization

Distinct synthetic repositories may remain when they prove genuinely different
public behavior. GitHub Actions must not enumerate them individually; the
configured `acceptance_suite` owns that sequence.

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

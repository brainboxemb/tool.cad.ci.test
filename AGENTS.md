# Repository instructions

## Purpose

`tool.cad.ci.test` is the permanent external black-box acceptance repository
for one released `tool.cad.ci` + `lib.py.cad.ci` stack.

It is also the living reference consumer for the normal CAD-CI repository
setup defined by `tool.cad.ci` Change 0001.

Keep it synthetic and domain-neutral. Do not add Forge, SolidCraft or product
CAD behavior. Minimal real CAD-engine smoke geometry is allowed only when a
released generic builder contract requires it.

## Consumer architecture

This repository must look like a normal consumer:

```text
.github/workflows/ci.yml
  -> one released shared CAD-CI route for the triggering event
       -> root cad-ci.yml
            -> repository-owned builders/items
```

The normal event contract is:

```text
pull request
  -> build / test / verify
  -> publish nothing

push main/dev-cad/dev-ci
  -> build / test / verify
  -> publish complete branch build + configured Pages

manual
  -> full | item | changed_paths
  -> build / test / verify
  -> publish nothing
```

Do not add a second planner, publisher, root composite-action path, local
bootstrap copy or second CAD-CI graph.

The reusable workflow release tag is the consumer release identity. All normal
routes must use the same accepted `tool.cad.ci` release.

## Permanent branches

`main`, `dev-cad` and `dev-ci` are permanent branches.

- short-lived issue/feature PRs may target a development branch and are
  squash-merged;
- direct development-branch -> `main` and `main` -> development-branch
  synchronization preserve history with merge commits;
- permanent branches are never auto-deleted;
- consume released branch/merge policy; do not implement local branch-policy
  logic.

## Live GitHub integration

`test_roots/*` do not prove GitHub trigger behavior. Real PR, push, manual and
merge contracts require actual GitHub state in this repository.

For live scenarios:

- use real branches, PRs and workflow dispatches;
- use only released public CAD-CI workflows;
- never replace a scenario with mocked event payloads or local copies of the
  workflow implementation;
- keep all normal CI routes on one accepted tool release;
- record mutable evidence in GitHub issues/PRs/Actions, not stable specs.

## Black-box boundary

Acceptance may invoke public released CLI/workflow behavior only.

Do not import or reproduce library planner, SCons, cache, build-store or
publication internals. Small test helpers may inspect public process/file
results only.

If acceptance finds a generic gap, return to the owner repository. Do not add a
local workaround.

## Case organization

Standalone synthetic consumer repositories live under:

```text
test_roots/
  001_name/
  002_name/
  ...
```

Use three-digit numeric prefixes. Every root owns its own `cad-ci.yml`.

Distinct synthetic roots remain only when they prove genuinely different
public behavior. GitHub Actions must not enumerate them individually.

Every registered case root has a local `README.md` describing status, purpose,
public contract, fixture/method and failure ownership.

Source-text assertions that merely freeze private workflow implementation are
not acceptance. Prefer observable public behavior.

## Publication

Synthetic publication cases under `test_roots/*` use an isolated local Git
remote and never mutate this repository's real generated branches.

Live branch-build acceptance uses only the reserved namespace:

```text
test-output/build
test-output/gh-pages
```

Never use normal `build` or `gh-pages` refs merely for acceptance.

## Development process

One logical change uses one issue, one branch and one pull request.

`docs/plan.md` contains unfinished work only. Keep mutable issue/release state
there instead of duplicating it in stable requirements/design text.

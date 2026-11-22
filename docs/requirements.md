# External CAD-CI acceptance requirements

## Released consumer path

- The repository consumes one released `tool.cad.ci` version tag.
- GitHub Actions uses only the normal public `reusable-ci.yml` entrypoint.
- The called tool pins the exact released `lib.py.cad.ci` revision.
- The acceptance repository does not clone/install a second tool copy.

## Permanent lane integration

- The repository owns permanent `main`, `dev-cad` and `dev-ci` branches.
- Pull requests use the released lane policy from `reusable-ci.yml`; there is
  no local classifier.
- Docs-only PRs into a development lane may use the released cheap path.
- Direct development-lane promotions to `main` run complete CAD-CI.
- Lane promotion/synchronization preserves history with merge commits.
- Permanent lanes must not be auto-deleted after merge.
- The released merge-policy workflow may dispatch the same `ci.yml` after a
  merge; manual/dispatch runs execute complete acceptance.

## Config-driven suite

- Root `cad-ci.yml` is the top-level CI configuration.
- GitHub Actions does not enumerate individual acceptance cases.
- One configured acceptance-suite step runs the black-box cases.
- Repository variables must reach consumer commands and override inherited
  non-secret caller values according to the released contract.

## Black-box behavior

Cases exercise public CLI/workflow behavior only. The suite covers distinct
contracts for selection, execution, dependencies, partial runs, process
participation, outputs/cache, failures/timeouts, parallel jobs and durable
publication.

A case must not reproduce planner, SCons, build-store or publication decisions
in test helpers.

## Workflow behavior

A successful complete acceptance run proves that another repository can call
the released high-level workflow and execute its root `cad-ci.yml` through the
released tool/library stack.

Internal workflow source layout is not an acceptance contract. Do not freeze
private step names or helper implementation with source-text assertions.

## Publication isolation

Build/Page publication cases use an isolated local Git remote and must not
mutate this repository's real generated branches.

## Governance API

Merge-governance acceptance remains separately identified from CAD-CI
execution. It may inspect/execute the released governance helper against a fake
GitHub API because that API is not part of the normal CAD-CI graph.

## Completion

A candidate tool release is accepted only when the complete config-driven suite
is green through the released reusable workflow. Consumer repositories may
migrate only after that result.

# External CAD-CI acceptance requirements

## Reference consumer

`tool.cad.ci.test` is both:

- external black-box acceptance for an exact released CAD-CI stack; and
- the living normal-consumer reference from `tool.cad.ci` Change 0001.

A normal repository should be able to copy/adapt the root workflow structure
without inheriting acceptance-specific orchestration.

## Released consumer path

- All normal routes pin one exact released `tool.cad.ci` version.
- The released tool pins the exact `lib.py.cad.ci` revision.
- The consumer does not clone/install another tool copy.
- Root `cad-ci.yml` owns repository items/builders.
- GitHub workflow YAML owns only triggers, permissions and routing to released
  public workflows.

## Pull request

A pull request:

- tests the exact PR head;
- uses released affected-item and branch-policy behavior;
- builds/tests/verifies only;
- publishes no generated build or Pages state.

## Permanent branch integration

A permanent branch build is triggered by either:

- a normal push to `main`, `dev-cad` or `dev-ci`; or
- the shared merge-policy integration dispatch on that branch.

The merge-policy dispatch is created with `GITHUB_TOKEN` and therefore reaches
the consumer as `workflow_dispatch` from `github-actions[bot]`. The consumer
routes that bot dispatch to the same branch-build path; it is not a human
manual run.

The branch build:

- uses the released permanent-branch build/publication workflow;
- publishes complete branch build output under the reserved
  `test-output/build` acceptance branch;
- publishes configured Pages output under `test-output/gh-pages`;
- records exact source provenance.

## Manual run

A human `workflow_dispatch` is read-only.

It exposes one explicit mode:

- `full`;
- `item`;
- `changed_paths`.

Manual execution must never enter permanent-branch publication.

## Config-driven suite

- Root `cad-ci.yml` is the top-level CAD-CI configuration.
- GitHub Actions does not enumerate individual acceptance cases.
- Repository variables reach consumer commands according to the released
  contract.

## Black-box behavior

Cases exercise public CLI/workflow behavior only. They do not reproduce planner,
SCons, build-store or publication decisions in test helpers.

## Publication isolation

Synthetic publication cases use isolated local Git remotes.

Live publication acceptance uses only `test-output/*` generated refs.

## Governance API

Merge governance is separate from CAD-CI execution. Do not mix merge-policy
experiments into the normal PR/push/manual consumer workflow.

## Completion

A released stack is accepted only when the normal reference workflow and
required black-box cases are green. Real consumers migrate only after that
result.

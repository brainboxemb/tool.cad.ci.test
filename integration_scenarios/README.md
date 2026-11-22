# Live GitHub integration scenarios

Status: current

This directory defines the acceptance contracts that cannot be proven by the
synthetic repositories below `test_roots/`.

## Boundary

`test_roots/*` prove repository configuration, builder resolution, CLI,
selection, SCons execution, caching and publication behavior in disposable
synthetic repositories.

`integration_scenarios/*` prove the GitHub delivery layer with **real GitHub
state**:

- branch creation;
- pull-request events;
- reusable-workflow invocation;
- permanent-lane classification;
- issue-comment merge commands;
- merge commits;
- post-merge workflow dispatch.

A scenario is not accepted by calling the CLI locally or by mocking a GitHub
event. The branch, pull request, comment and Actions run must actually exist in
this repository.

## Scenarios

| Scenario | Contract |
| --- | --- |
| [001_feature_pr](001_feature_pr/README.md) | Short-lived non-doc branch -> development lane triggers full reusable CI. |
| [002_docs_only_pr](002_docs_only_pr/README.md) | Docs-only PR -> development lane takes released cheap path. |
| [003_lane_promotion](003_lane_promotion/README.md) | Permanent lane -> main forces full CI and history-preserving merge. |
| [004_lane_sync](004_lane_sync/README.md) | main -> permanent lane preserves lane history and dispatches full post-merge CI. |
| [005_merge_comment](005_merge_comment/README.md) | Real `/merge` issue-comment trigger invokes released merge-policy workflow. |

## Version contract

`.github/workflows/ci.yml` and `.github/workflows/merge-policy.yml` must use
the same accepted released `tool.cad.ci` version.

Current accepted version: `v0.25.0`.

## Evidence

Mutable execution evidence belongs in GitHub PRs/issues/Actions and the current
`docs/plan.md`, not in these stable scenario specifications.

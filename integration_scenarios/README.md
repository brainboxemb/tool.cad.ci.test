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
- permanent-branch classification;
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
| [003_lane_promotion](003_lane_promotion/README.md) | Permanent development branch -> main forces full CI and history-preserving merge. |
| [004_lane_sync](004_lane_sync/README.md) | main -> permanent development branch preserves lane history and dispatches full post-merge CI. |
| [005_merge_comment](005_merge_comment/README.md) | Real `/merge` issue-comment trigger invokes released merge-policy workflow. |
| [006_durable_workflow](006_durable_workflow/README.md) | Released durable workflow publishes stable/named build + Pages to reserved `test-output/*` refs. |
| [007_release_workflow](007_release_workflow/README.md) | Released CAD release workflow refuses a stale source, then publishes the exact stable source after checking `test-output/build/main/build.json`. |

## Version contract

`.github/workflows/ci.yml` and `.github/workflows/merge-policy.yml` must use
the same accepted released `tool.cad.ci` version.

Current full adopted baseline: `v0.34.2`. Focused v0.35.0 targeted-selection acceptance completed under issue #254 without changing the adopted repository wrappers. Issue #256 now qualifies v0.36.0 and the new central CAD release workflow. Durable live publication remains isolated on `test-output/build` and `test-output/gh-pages`.

## Evidence

Mutable execution evidence belongs in GitHub PRs/issues/Actions and the current
`docs/plan.md`, not in these stable scenario specifications.

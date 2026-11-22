# Permanent lane integration

Status: current

This repository is the external integration consumer for the standard
`tool.cad.ci` permanent-lane contract.

## Branches

```text
main
dev-cad
dev-ci
```

All three are permanent branches. GitHub repository settings must therefore
keep `delete_branch_on_merge=false` and allow merge commits.

## PR paths

### Short-lived work -> development lane

Normal issue/feature branches target `dev-cad` or `dev-ci` when the work is
being integrated through that lane.

These PRs are temporary work and use squash merge.

### Docs-only PR -> development lane

The released lane policy receives:

```json
{
  "stable_ref": "main",
  "lane_refs": ["dev-cad", "dev-ci"],
  "docs_only_prefixes": ["docs/"]
}
```

A non-empty PR diff entirely below `docs/` may take the released cheap path.
The classification stays in `tool.cad.ci`; this repository has no local
classifier.

### Development lane -> main

A direct `dev-cad -> main` or `dev-ci -> main` promotion PR must run complete
CAD-CI. The merge policy uses a history-preserving merge commit rather than
squash.

### main -> development lane

Synchronization back from `main` into a permanent development lane also uses
history-preserving merge behavior. The lane must remain after the merge.

## Merge command

`.github/workflows/merge-policy.yml` consumes the released merge-policy
workflow. Owner-issued `/merge` is the integration command.

After merge, the policy dispatches `ci.yml`. Its `workflow_dispatch` path
sets `full_run=true`, so post-merge integration validation is complete without
adding another CI implementation.

## Cheap-path verification

A documentation-only pull request into `dev-cad` or `dev-ci` must contain a
non-empty diff entirely below `docs/`. The released lane classifier should
then report successful docs-only validation before Python/tool/library
bootstrap. This repository does not duplicate that classification locally.

A docs-only probe is valid only when the changed paths are all beneath
`docs/`; changes to workflows, root configuration or acceptance fixtures must
run normal CAD-CI.

## What this repository proves

The repository provides real GitHub evidence for:

- permanent lane survival;
- canonical lane PR classification;
- docs-only cheap validation;
- full lane promotion validation;
- history-preserving lane promotion/synchronization;
- post-merge integration dispatch.

Do not add local lane classification or a second workflow implementation.

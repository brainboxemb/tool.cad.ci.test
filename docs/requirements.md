# External CAD-CI test requirements

## Exact released stack

- Every test uses one exact released `tool.cad.ci` commit.
- The reusable workflow and direct bootstrap must use the same tool commit.
- Moving branches or unreleased tool revisions are not accepted.

## Public behavior

The repository must test the released stack from outside its implementation.

The suite covers:
- normal build/current behavior;
- changed-item selection;
- dependencies and fan-out;
- partial runs;
- directory output and SCons CacheDir behavior;
- timeout/failure behavior;
- durable build and Pages publication;
- high-level reusable workflow execution and output handoff;
- reusable-workflow authentication to GitHub Container Registry;
- item-level `process` participation through the released library/tool stack.

For repository variables:
- root `cad-ci.yml:variables` must reach the consumer command;
- when the caller supplies the same non-secret environment name, the repository
  value must override it;
- CAD-CI implementation details are not reproduced in the test repository.

## Process selection

The external suite must prove released item participation without reproducing
selection logic:

- omitted `process` behaves as processed;
- `process: false` is absent from a full plan and full run;
- a processed item still runs and materializes normal evidence/output;
- explicit execution of a non-processed item fails clearly;
- the acceptance case checks observable CLI/output behavior only.

## Completion

A tool release is externally tested only when the complete suite is green on
the exact pinned release. Forge/CAD must not adopt the release before that.


## GHCR workflow authentication

The external reusable-workflow case must prove released tool 0.10.0 prepares
Docker authentication before the consumer CAD-CI command runs.

Acceptance rules:

- the caller grants `packages: read`;
- the real consumer command checks the runner's Docker configuration;
- `ghcr.io` must have an authentication entry;
- the test checks only presence of that entry;
- the credential value must not be printed, decoded, copied into build output or
  exposed as consumer environment;
- the test does not name or pull a Forge/SolidCraft image.

This proves generic workflow credential setup without adding domain behavior to
the acceptance repository.


## Acceptance event policy

The complete black-box suite runs automatically on `pull_request`.

A normal `push` to `main` must not automatically repeat the same complete
suite after an already-green pull request merge.

`workflow_dispatch` provides an explicit way to run the same suite against
main when a main-only condition genuinely requires verification.

## Generated-branch isolation

The durable build and Pages publication case must exercise the released tool's
real generated-branch commands against an isolated Git remote created inside the
runner.

Acceptance must still prove:

- `build` branch creation/update/fetch;
- `gh-pages` stable or preview publication;
- source freshness rejection;
- PR cleanup behavior;
- evidence fetched back from the generated build branch.

The case must not push generated branches to the real
`brainboxemb/tool.cad.ci.test` repository.

The acceptance workflow therefore requires only read access to repository
contents plus the existing package-read permission.


## Tool 0.12.1 maintenance acceptance

External acceptance of tool 0.12.1 must prove:

- the exact tool commit is `0e7d8a876d95484a4c8870356f3b0ca67e5e493b`;
- public item evidence schema is 2 and includes run timestamps;
- public step evidence schema is 3 and includes run timestamps plus action
  timestamps when the action executes;
- timeout/failure actions expose action timestamps;
- high-level reusable CI owns superseded-run cancellation;
- lower-level reusable plan/run workflows do not own that high-level
  concurrency group;
- durable build preparation accepts current item evidence schema 2 while legacy stored schema 1 remains readable.


## Removed durable main item acceptance

The existing publication acceptance must prove the released stack distinguishes
an unselected current item from an item removed from current configuration.

Starting from a durable main baseline with two configured items A and B:

- a disposable current consumer configuration removes B;
- a deletion-only `build update-main` selects no replacement item, keeps A
  current and removes B from output and manifest;
- A's owned result/evidence bytes remain unchanged in that deletion-only update;
- a separate mixed update selects/replaces A while also removing B;
- the test invokes only released public CLI commands and inspects generated
  output;
- no test helper compares manifests to decide deletion or removes durable output
  on behalf of CAD-CI.


## Selective-startup released-stack acceptance

The external suite must prove the released selective-run preparation behavior
without importing library internals or asserting a machine-specific wall time.

A synthetic consumer repository must contain:
- one selected item and one direct dependency;
- unrelated processed items;
- an unrelated processed item whose configured input matches a symlink.

Required public behavior:
- `cad-ci run --item <selected>` succeeds and materializes normal selected and
  dependency output/evidence;
- the unrelated matched symlink does not affect that selective run;
- explicitly running the symlink-owning item still fails with the normal
  configured-source symlink safety error;
- the case invokes only the exact released tool CLI.

This acceptance proves that inactive targets no longer participate in source
input preparation while preserving active-target source safety.


## Released bounded-jobs acceptance

The external suite must prove the exact released tool's opt-in parallel-jobs
surface without importing CAD-CI internals.

- direct bootstrap, reusable workflow and same-runner action pin the same exact
  released tool revision;
- reusable workflow and composite action must successfully accept `jobs: 2`;
- a synthetic repository with two independent targets must run through the
  released CLI with `--jobs 2`;
- public step evidence for both targets must contain successful BUILT outcomes
  plus non-null action `started_at` / `finished_at` values;
- the two action intervals must overlap, proving actual concurrent execution;
- no fixed elapsed-time threshold is an acceptance requirement;
- default jobs=1 behavior remains covered by the existing suite and remains the
  compatibility baseline.

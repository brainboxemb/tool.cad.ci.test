# External CAD-CI test design

`tool.cad.ci.test` is an external consumer of one exact released
`tool.cad.ci` revision. It does not implement CAD-CI behavior.

## Release identity

`dependencies.repos` pins the exact tool commit used by direct CLI cases.
The GitHub workflow calls the reusable workflow from that same exact commit.
The tool itself pins one exact released `lib.py.cad.ci` revision.

This gives one unambiguous tool/library stack for every test run.

## Test cases

Each top-level case is a small synthetic consumer repository. Cases exercise
public behavior only through the released CLI or reusable workflow.

The root `workflow_case` specifically tests the reusable workflow boundary.
For repository-variable support it supplies one caller environment value and
declares a different value with the same name in root `cad-ci.yml`. The
consumer command must observe the repository value.

This verifies the public precedence without copying variable parsing or merge
logic into this repository.

## Process selection acceptance

A dedicated `process_case` is a synthetic consumer repository with one normal
item and one `process: false` item.

Its `check.py` invokes only the released CLI through `tests/support.py` and
asserts the public results:

- a full JSON plan contains only the processed item;
- a full run materializes only that item's output/evidence;
- no build output is created for the non-processed item;
- an explicit run of the non-processed item exits with the documented error.

The case does not import library planner/config modules and does not calculate
selection independently.

## Failure boundary

If a case exposes missing generic behavior, implementation returns to
`lib.py.cad.ci` or `tool.cad.ci`. This repository may add a failing example,
but not a local workaround.


## GHCR authentication acceptance

The root `workflow_case` remains the black-box reusable-workflow consumer.

Its command runs inside the released workflow after generic setup and checks:

```text
~/.docker/config.json
  -> auths
     -> ghcr.io exists
```

The check does not inspect the authentication value. Presence is sufficient to
prove that the released workflow executed Docker login before invoking
`cad-ci run`.

The caller workflow grants `packages: read` and calls
`reusable-ci.yml` at the same exact commit stored in `dependencies.repos`.

The test intentionally does not pull a real CAD/domain image. Package
availability and image selection are consumer concerns; this repository proves
only the generic authenticated-runner contract.


## Acceptance-run ownership

Pull-request CI is the authoritative automatic external acceptance result.

The workflow deliberately has no automatic `push: main` trigger. A squash
merge changes the commit SHA but does not justify re-running every black-box
case against the same pinned external tool stack. `workflow_dispatch` keeps a
manual main verification path for exceptional cases.

## Isolated publication remote

`publish_case` creates:

```text
output/publish_case/remote.git   bare remote
output/publish_case/repository   working clone
```

The current event source commit is pushed from the checked-out acceptance
repository into the isolated remote under the event source branch name. The
working clone is then used as `--repo` for every released publication command.

The tool therefore performs real Git branch publication, freshness checks,
fetches and cleanup, but no write reaches the GitHub repository. This preserves
the public publication contract without triggering GitHub Pages.


## 0.12.1 maintenance stack

The test repository accepts timing evidence only by reading generated public
evidence from the released stack. It does not import or reproduce timing logic.

Concurrency acceptance inspects the exact released workflow files after
bootstrap: only the high-level reusable workflow may own the normal-consumer
concurrency group.


## Removed-item publication acceptance

`publish_case` reuses its existing two-item synthetic consumer.

It first prepares a normal durable main baseline for A+B. It then creates a
disposable source copy whose current configuration contains only A by removing
the source directory for B.

Two released CLI calls are exercised independently from the same baseline:

```text
deletion-only:
  update-main --changed items/b/ci.yml
  current config: A
  selected replacements: none
  expected durable result: A only, A bytes unchanged

mixed:
  update-main --changed items/a/run.py
  current config: A
  selected replacements: A
  expected durable result: A replacement only
```

The acceptance code performs only source-fixture setup and assertions. Durable
membership/deletion is performed entirely by the released stack.


## Selective-startup acceptance case

`selective_startup_case/check.py` creates its complete synthetic consumer under
the ignored disposable output tree at runtime.

It intentionally creates an unrelated source symlink after writing normal
configuration. The case then invokes only the bootstrapped released CLI:

```text
run --item selected
  -> dependency + selected output/evidence must succeed

run --item symlink-owner
  -> documented source-input symlink error
```

No test code imports `cad_ci`, reads the private SCons manifest or calculates
the active closure. The inactive-symlink distinction is observable released
behavior and therefore proves the optimization boundary without duplicating its
implementation.

Additional unrelated items may be generated to retain a repository shape where
whole-graph source preparation would be materially wasteful, but acceptance is
based on behavior rather than elapsed seconds.


## Bounded-jobs black-box proof

Parallel execution is observed only through public consumer evidence.

The synthetic acceptance repository contains two independent SCons targets.
The exact released CLI runs the repository with `--jobs 2`, then the test reads:

```text
build/left/.cad-ci/steps/build.json
build/right/.cad-ci/steps/build.json
```

Each record must report a successful executed action. The two
`started_at` / `finished_at` intervals must overlap.

This distinguishes real SCons concurrency from a tool that merely accepts or
forwards a jobs argument. It avoids copying scheduler logic into the acceptance
repository and avoids machine-specific wall-clock thresholds.

The reusable workflow and same-runner action are separately invoked with jobs=2
in the normal acceptance workflow to prove their public input forwarding.

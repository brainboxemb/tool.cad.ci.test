# tool.cad.ci.test

Permanent external black-box acceptance repository for released
`tool.cad.ci` + `lib.py.cad.ci`.

The repository is intentionally a normal consumer:

```text
.github/workflows/ci.yml
  -> tool.cad.ci reusable-ci.yml@v0.24.0
       -> root cad-ci.yml
            -> acceptance-suite
                 -> public cad_ci_tool CLI
                 -> test_roots/NNN_name standalone consumer repositories
```

There is no second checkout/install of `tool.cad.ci`, no root-action test
route and no local CI implementation.

## Acceptance suite

`cad-ci.yml` contains one top-level `acceptance_suite` item. Its configured
Python step runs the synthetic black-box cases against the exact tool/library
stack already loaded by the released reusable workflow.

The cases cover distinct public behavior such as:

- minimal cold/current/rebuild execution;
- changed-item selection;
- nested configuration and output ownership;
- dependency fan-out and dependency-output copy;
- partial reruns and process participation;
- bounded SCons jobs;
- directory outputs, cache restore, timeouts and failures;
- durable build/Page publication against an isolated local Git remote;
- the separately identified merge-governance API.

The suite may spawn the public CLI because this repository tests the released
stack from outside. It must not import planner/SCons/build-store internals or
reimplement their decisions.

## Test roots

Standalone synthetic consumer repositories live under `test_roots/` and use a
three-digit stable order: `001_simple`, `002_...`, `003_...`.

Each test root owns its own `cad-ci.yml`. The local README is the maintenance
contract for that root.

## Case index

| Case | Status |
| --- | --- |
| [workflow_case](workflow_case/README.md) | current |
| [001_simple](test_roots/001_simple/README.md) | current |
| [002_selection](test_roots/002_selection/README.md) | current |
| [003_fresh_runner](test_roots/003_fresh_runner/README.md) | current |
| [004_nested_items](test_roots/004_nested_items/README.md) | current |
| [005_nested_publish](test_roots/005_nested_publish/README.md) | current |
| [006_dependencies](test_roots/006_dependencies/README.md) | current |
| [007_dependency_copy](test_roots/007_dependency_copy/README.md) | current |
| [active_dependents_case](active_dependents_case/README.md) | current |
| [partial_rerun_case](partial_rerun_case/README.md) | current |
| [process_case](process_case/README.md) | current |
| [parallel_jobs_case](parallel_jobs_case/README.md) | current |
| [directory_output_case](directory_output_case/README.md) | current |
| [timeout_case](timeout_case/README.md) | current |
| [publish_case](publish_case/README.md) | current |
| [merge_policy_case](merge_policy_case/README.md) | separate API; temporary here |

[acceptance_suite](acceptance_suite/README.md) documents how cases are
registered and which status is allowed.

## Workflow and lane boundary

The repository is also the external integration consumer for the standard
permanent branch layout:

```text
main
dev-cad
dev-ci
```

The GitHub workflow still contains one normal consumer call. Pull requests use
the released lane policy; manual/post-merge dispatches request a complete run:

```yaml
jobs:
  acceptance:
    uses: brainboxemb/tool.cad.ci/.github/workflows/reusable-ci.yml@v0.24.0
    with:
      pr_policy_json: '{"stable_ref":"main","lane_refs":["dev-cad","dev-ci"],"docs_only_prefixes":["docs/"]}'
      full_run: ${{ github.event_name == 'workflow_dispatch' }}
      jobs: 2
```

See [permanent lane integration](docs/background/lane-integration.md) for the
real PR/merge scenarios exercised by this repository.

Repository variables in root `cad-ci.yml` are also used to prove that
repository configuration reaches consumer commands and overrides inherited
non-secret caller values.

## Safety boundary

Generated build/Page publication acceptance uses only an isolated local Git
remote created during the test. It never pushes generated branches to this
repository.

If a case exposes missing generic behavior, fix and release the owning
`lib.py.cad.ci` or `tool.cad.ci` repository. Do not patch around it here.

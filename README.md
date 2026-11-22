# tool.cad.ci.test

Permanent external black-box acceptance repository for released
`tool.cad.ci` + `lib.py.cad.ci`.

The repository is intentionally a normal consumer:

```text
.github/workflows/ci.yml
  -> tool.cad.ci reusable-ci.yml@v0.23.0
       -> root cad-ci.yml
            -> acceptance-suite
                 -> public cad_ci_tool CLI
                 -> synthetic case repositories
```

There is no second checkout/install of `tool.cad.ci`, no root-action test
route and no local CI implementation.

## Acceptance suite

`cad-ci.yml` contains one top-level `acceptance_suite` item. Its configured
Python step runs the synthetic black-box cases against the exact tool/library
stack already loaded by the released reusable workflow.

The cases cover distinct public behavior such as:

- cold/current and changed-input execution;
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

## Case index

The local README in each case is the maintenance contract for that case.

| Case | Status |
| --- | --- |
| [workflow_case](workflow_case/README.md) | current |
| [simple_case1](simple_case1/README.md) | current |
| [more_complex_case2](more_complex_case2/README.md) | current; historical directory name |
| [fresh_runner_case](fresh_runner_case/README.md) | current |
| [nested_item_case](nested_item_case/README.md) | current |
| [nested_publish_case](nested_publish_case/README.md) | current |
| [dependency_case](dependency_case/README.md) | current |
| [dependency_copy_case](dependency_copy_case/README.md) | current |
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

## Workflow boundary

The GitHub workflow contains one normal consumer call:

```yaml
jobs:
  acceptance:
    uses: brainboxemb/tool.cad.ci/.github/workflows/reusable-ci.yml@v0.23.0
    with:
      full_run: true
      jobs: 2
```

Repository variables in root `cad-ci.yml` are also used to prove that
repository configuration reaches consumer commands and overrides inherited
non-secret caller values.

## Safety boundary

Generated build/Page publication acceptance uses only an isolated local Git
remote created during the test. It never pushes generated branches to this
repository.

If a case exposes missing generic behavior, fix and release the owning
`lib.py.cad.ci` or `tool.cad.ci` repository. Do not patch around it here.

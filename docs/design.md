# External CAD-CI acceptance design

`tool.cad.ci.test` deliberately contains no second CI architecture.

## Permanent branch topology

```text
main
├── dev-cad
└── dev-ci
```

`dev-cad` and `dev-ci` are permanent integration lanes, not disposable
feature branches. Short-lived work may target a lane with squash merge.
Lane-to-`main` promotion and `main`-to-lane synchronization use the released
merge-governance contract and preserve history.

The repository consumes the released lane PR classifier through
`pr_policy_json`; it does not reproduce lane logic in local YAML.

## Runtime topology

```text
GitHub pull request / manual dispatch
  -> reusable-ci.yml@released-version
       -> exact tool source
       -> tool-pinned lib.py.cad.ci source
       -> cad_ci_tool run
            -> root cad-ci.yml
                 -> acceptance-suite
                      -> public CLI black-box cases
```

The outer run proves the normal consumer workflow boundary. The inner
black-box CLI calls prove detailed released behavior against disposable
synthetic case repositories.

The same loaded `cad_ci_tool` source is used by every case; there is no
`ext/cad-ci` clone, editable install or second release pin.

## Acceptance-suite step

The suite runner loads each case's `main()` in one configured Python step.
Cases remain independently readable and may invoke the public CLI in child
processes where process isolation is part of the observable behavior.

This keeps GitHub workflow orchestration constant while preserving independent
synthetic repositories for contracts that require different root
`cad-ci.yml` configurations.

## Tool identity

The workflow release tag identifies the released tool. Tests may inspect the
loaded tool's `VERSION` and pinned library dependency when release identity is
itself part of the contract.

## Publication

Publication tests create a disposable local bare Git remote. Real released
publication commands operate against that remote, so branch/freshness behavior
is exercised without mutating GitHub state.

## Separate governance surface

Merge policy is not CAD-CI execution. Its acceptance remains an explicit
separate case until that API is moved or removed from `tool.cad.ci`.

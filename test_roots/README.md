# Test roots

This directory contains standalone synthetic consumer repositories used for
external CAD-CI acceptance.

## Naming

Use a stable three-digit prefix:

```text
001_simple/
002_selection/
003_dependencies/
...
```

The number is ordering, not a release or schema version.

## Root contract

Every test root is independently understandable and owns at least:

```text
README.md
cad-ci.yml
check.py
```

Add `ci.yml`, source files and helper scripts required by that consumer.

The root `cad-ci.yml` in each test root is the configuration under test. The
top-level `tool.cad.ci.test/cad-ci.yml` is only the acceptance harness and must
not substitute for a test root's own configuration.

Each root should prove one coherent public use case. Do not turn one numbered
root into a grab bag of unrelated behaviors.

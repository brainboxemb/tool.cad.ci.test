# 011 shared builder

Status: current

## Purpose

External black-box proof that normal item `ci.yml` can stay declarative while
multiple items share one repository-owned builder implementation.

## Repository contract

This directory is a self-contained synthetic consumer repository:

```text
011_shared_builder/
  cad-ci.yml
  ci/builders/shared/
    builder.yml
    build.py
  items/a/
    ci.yml
    input.txt
  items/b/
    ci.yml
    input.txt
  check.py
```

Root `cad-ci.yml` names the builder. Each item selects it with
`builder: shared`. Executable steps exist only in the builder directory.

## Public contract

The case proves:

1. two items use one shared builder without item-local `steps` or `run`;
2. the released CLI builds both items;
3. builder commands receive `CAD_CI_BUILDER`, `CAD_CI_BUILDER_PATH` and
   `CAD_CI_ITEM_PATH`;
4. a changed builder path selects both using items;
5. changing shared builder implementation rebuilds both outputs.

## Failure ownership

Builder configuration loading, selection and SCons invalidation belong in
`lib.py.cad.ci`. Public CLI/workflow exposure belongs in `tool.cad.ci`.

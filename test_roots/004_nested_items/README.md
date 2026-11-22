# 004 nested items

Status: current

## Purpose

Standalone consumer repository for nested item discovery, templates and Git
selection using a declarative shared builder.

## Public contract

The case proves:

1. root templates apply to nested items discovered by `examples/*/*`;
2. the template selects a repository-owned `reference` builder;
3. child-local source/input changes select only that nested child;
4. parent-relative shared contract inputs can select both nested siblings;
5. repo-relative shared inputs remain available to the builder;
6. explicit base/head selection works from fresh clones with no generated state.

## Declarative builder contract

`cad-ci.yml` owns the `reference` builder alias and template. The template
contains only kind, builder selection and watch configuration; it contains no
executable `steps:` or `run:`.

Each nested child `ci.yml` remains only:

```yaml
template: reference
```

The shared builder owns the executable step, input declaration and
`result.txt` output. The child `model.py` files are model source, not build
orchestration.

## Fixture

Two nested child items live below `examples/attach-angle/`. They inherit one
root template and share a parent verification contract plus repository-level
input.

## Failure ownership

Template inheritance, builder resolution, path normalization and Git selection
belong in `lib.py.cad.ci`.

Durable nested publication/output ownership is intentionally not tested here.

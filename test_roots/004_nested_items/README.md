# 004 nested items

Status: current

## Purpose

Standalone consumer repository for nested item discovery, templates and Git
selection.

## Public contract

The case proves:

1. root templates apply to nested items discovered by `examples/*/*`;
2. child-local source/input changes select only that nested child;
3. parent-relative shared contract inputs can select both nested siblings;
4. repo-relative shared inputs remain available to nested item commands;
5. explicit base/head selection works from fresh clones with no generated state.

## Fixture

Two nested child items live below `examples/attach-angle/`. They inherit one
root template and share a parent verification contract plus repository-level
input.

## Failure ownership

Nested configuration/path normalization and Git selection belong in
`lib.py.cad.ci`.

Durable nested publication/output ownership is intentionally not tested here.

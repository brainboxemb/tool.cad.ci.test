# Nested item case

Status: current

## Purpose

Prove nested item discovery, root templates, local/parent-relative inputs and
Git selection.

## Public contract

A child-local change selects only that child; a shared parent contract can
select the appropriate nested siblings without generated state from a previous
runner.

## Fixture and method

The fixture models nested CAD-style items, commits controlled changes and runs
the public CLI from fresh clones.

## Failure ownership

Configuration/path normalization and selection belong in `lib.py.cad.ci`.

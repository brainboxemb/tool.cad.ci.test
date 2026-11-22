# 008 active direct dependents

Status: current

## Purpose

Standalone consumer repository for public
`selection_context: direct_dependents` behavior using declarative builders.

## Public contract

The case proves:

1. selecting only consumer A exposes only A to the shared producer;
2. repeating the same selection is current;
3. selecting only consumer B changes the producer's active-dependent context
   and target-spec identity;
4. changing the producer input selects both direct consumers while executing the
   shared producer once;
5. a full run exposes both active consumers while unrelated work remains
   independent.

## Declarative builder contract

`cad-ci.yml` defines two builder aliases:

- `batch-context` owns the producer step and
  `selection_context: direct_dependents`;
- `verify-item` is shared by consumer-a, consumer-b and unrelated.

Item `ci.yml` files contain only identity/kind, builder selection, dependency
and watch configuration. They contain no executable `steps:` or `run:`.

The shared verify builder uses `CAD_CI_ITEM` to produce item-specific output,
so the three former item-local `run.py` files are unnecessary.

## Fixture

`batch` is a shared producer. `consumer-a` and `consumer-b` depend on it.
`unrelated` proves that unrelated work does not enter the direct-dependent
context.

## Failure ownership

Selection context, builder resolution and target-signature semantics belong in
`lib.py.cad.ci`.

Ordinary dependency traversal is covered by `test_roots/006_dependencies`.

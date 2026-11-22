# 005 nested publication

Status: current

## Purpose

Standalone consumer repository for durable build-store ownership when a parent
item and nested child item coexist, using one shared declarative builder.

## Public contract

The case proves:

1. complete main scope contains both parent and nested-child outputs/evidence;
2. sparse PR overlays may select both owners or only the nested child;
3. a parent-only main update preserves the unselected child output/evidence;
4. a child-only main update preserves the unselected parent output/evidence;
5. nested paths remain correctly represented in public build manifests.

## Declarative builder contract

Both parent and child use `builder: nested-output`. Their item `ci.yml`
files contain only identity, kind, builder selection and item-local watch
configuration.

The shared builder owns `input.txt`, the execution command and one
builder-owned `result.txt` output. The same output name is intentionally used
inside each independent item output root; this test is about ownership/path
boundaries, not item-specific filename conventions.

## Fixture

A parent item lives at `items/model`; its child lives at
`items/model/reference`. Both own independent declared output/evidence.

## Failure ownership

Durable build-store ownership, sparse update semantics and builder resolution
belong in `lib.py.cad.ci`.

Nested discovery/templates/Git selection are covered separately by
`test_roots/004_nested_items`.

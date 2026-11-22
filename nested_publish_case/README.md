# Nested publication case

Status: current

## Purpose

Prove durable output ownership when parent and nested child items coexist.

## Public contract

Complete and sparse scopes may contain parent and child outputs while updating
one item preserves the unselected neighbor's output/evidence.

## Fixture and method

The case builds parent/child items, prepares main/PR scopes and compares public
build manifests/evidence.

## Failure ownership

Durable build-store ownership belongs in `lib.py.cad.ci`.

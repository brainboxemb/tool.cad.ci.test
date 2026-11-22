# Durable publication case

Status: current

## Purpose

Prove the released durable build-store and Pages publication contract without
writing generated branches to GitHub.

## Public contract

The case covers complete main output, sparse PR output, resolved views,
removed-item updates, named scopes, source-freshness rejection, build-branch
publication and stable/named Pages subtrees.

## Fixture and method

The fixture builds two items and creates an isolated local bare Git remote.
Real public build/Page publication commands operate only against that remote.

## Failure ownership

Durable build/Page semantics belong in `lib.py.cad.ci`; CLI command exposure
belongs in `tool.cad.ci`.

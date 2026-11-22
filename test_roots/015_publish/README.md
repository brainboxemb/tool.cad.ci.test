# 015 durable publication

Status: current

## Purpose

Standalone consumer repository for the released durable build-store and Pages
publication contract, without writing generated branches to GitHub.

## Public contract

The case proves:

- complete main durable output;
- sparse PR overlays and resolved views;
- removed-item updates, including mixed changed+removed state;
- named durable scopes;
- source-freshness rejection before publication;
- real build-branch publication against an isolated local bare Git remote;
- stable and named Pages subtree preservation.

## Declarative builder contract

Both configured items select one repository-owned `publish-item` builder.
Item configs contain identity, kind and builder selection only.

The builder owns the executable build step and writes `result.txt` from the
current item directory name, preserving the observable `a` / `b` fixture
outputs without item-local `run.py` files.

The publication check itself uses only released public CLI commands and an
isolated local Git remote. It never writes generated branches to this GitHub
repository.

## Failure ownership

Durable build/Page semantics belong in `lib.py.cad.ci`; CLI command exposure
belongs in `tool.cad.ci`.

# 016 durable workflow consumer

Status: current

## Purpose

Standalone synthetic consumer for the config-driven complete durable
build/Pages contract used by the released permanent-branch workflow.

## Public contract

The case proves that a normal consumer can declare:

- one normal build item;
- one site-producing item;
- repository-owned builders;
- root `publication.pages` selecting the site item/output;
- complete stable and named build scopes;
- stable and named Pages filesystem layout without overwriting siblings.

The separate live GitHub scenario `integration_scenarios/006_durable_workflow`
proves the released reusable workflow and real generated Git refs.

## Fixture / method

The case runs only the public `cad_ci_tool` CLI from the exact released stack
already loaded by the outer acceptance workflow. It builds a disposable copy of
this synthetic repository, prepares complete `main` and `dev-ci` scopes and
installs stable/named Pages content into a disposable filesystem root.

Git publication/race behavior remains covered by `015_publish` against its
isolated local bare remote. This case never writes GitHub generated branches.

## Failure ownership

Root publication configuration, complete-scope preparation and Pages layout
belong in `lib.py.cad.ci`. CLI exposure belongs in `tool.cad.ci`; the live
workflow delivery boundary belongs in `integration_scenarios/006_durable_workflow`.

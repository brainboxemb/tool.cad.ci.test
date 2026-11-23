# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-23).

## Fully accepted baseline

- `tool.cad.ci v0.34.2` @
  `37f7a82c6769279d33367144c56976da89bb1a5d`;
- exact pinned `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`;
- `lib.py.cad.verification v0.16.0` @
  `c7c145b7be0c602724e8cca874ef29990baaad1e`;
- #248 completed Workplane + Assembly qualification and dev-ci/main/dev-cad
  durable provenance;
- live durable publication remains isolated on `test-output/*`.

## Candidate stack under acceptance

### #254 — accept v0.35.0 targeted read-only selection

**Now.**

Candidate released stack:

- `tool.cad.ci v0.35.0` @
  `9fcad92b7c5f10ae29a9cb085a4f25bb38ed00f9`;
- exact pinned `lib.py.cad.ci v0.18.2` @
  `088644a05ff698957aef2ddc6cc5de037ddfa158`.

Focused live gates on one short-lived PR to `dev-ci`:

1. exact `item: targeted-a` while `targeted-b` is configured to fail if
   accidentally selected;
2. one `changed_paths` JSON selection containing both A and B after B is
   switched to pass;
3. record exact head/run evidence and hand the released workflow to Forge #740.

This acceptance deliberately does not use the monolithic 001-019 suite as its
proof path. Root-granularity/performance cleanup remains #253.

## Boundary

This repository owns external acceptance evidence only. Targeted selection must
be supplied through the released public workflow. Do not copy planner logic,
toggle consumer `process` values, or publish durable state from a targeted
probe.

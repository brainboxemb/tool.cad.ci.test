# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22). This repository accepts the exact immutable CAD-CI tool/library
stack with independent generic consumer cases. It owns no CAD-CI algorithms.

## Released stack under acceptance

- `tool.cad.ci 0.21.0` @
  `b1474f6be66dc0236f2a5c2555af07a100447255`.
- `lib.py.cad.ci 0.11.1` @
  `fa6bf244381dde609a0b04de673d774911c52fea`.
- `dependencies.repos`, reusable workflows, advanced plan API, root action
  and merge-policy checks all use the exact released tool commit.
- The durable same-runner case now also executes the released 0.21.0 stack.

## Current work: #86 released-stack acceptance

Run the complete existing black-box suite against 0.21.0 / 0.11.1:

1. public `reusable-ci.yml` normal and no-output cases;
2. public advanced `reusable-plan.yml`;
3. root composite action run-only and durable same-runner paths;
4. one-job/one-runner `reusable-pr.yml` verification path;
5. merge-policy classification plus released `merge_command.py` behavior
   through an isolated fake GitHub API;
6. all CLI/SCons/build-store/Pages/publication consumer cases.

A failure is fixed in the owning tool/library repository, never patched around
here.

## Promotion gate

After this PR is green:
- merge it to `main` so the permanent acceptance baseline is 0.21.0 / 0.11.1;
- record the exact acceptance run in tool.cad.ci #110 and meta.cad.solidcraft #2;
- only then repin Forge/CAD consumers.

## Issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #86 Released-stack qualification | **now** | Complete exact 0.21.0 / 0.11.1 acceptance and merge the new baseline. |

Release-stability rules in `AGENTS.md` remain authoritative.

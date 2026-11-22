# Repository plan

Current source of truth for unfinished work in `tool.cad.ci.test`
(2026-11-22). This repository accepts the exact immutable CAD-CI tool/library
stack with independent generic consumer cases. It owns no CAD-CI algorithms.

## Accepted main baseline

- Released `tool.cad.ci 0.20.1` @
  `eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9`.
- Exact `lib.py.cad.ci 0.11.0` @
  `e621daf6e309bdd0e3f643a12007f1b66490696d`.
- Full accepted main run `45033890474` is green.
- `dependencies.repos` and the durable same-runner action remain unchanged.

## Current work: issue #86, candidate-only proof

The experimental [`tool.cad.ci` PR #111](https://github.com/brainboxemb/tool.cad.ci/pull/111)
is not yet a release. This isolated test PR invokes an **exact immutable
candidate commit**, not moving main.

- `consumer` / `no_output` call the candidate `reusable-ci.yml`. These
  are read-only tests of source bootstrap, one run, artifact and no-output
  contracts.
- The existing `same_runner` job remains on accepted 0.20.1 to avoid
  changing durable generated-branch behavior during draft qualification.
- `test` checks the accepted release as before, then checks the candidate
  `merge_command.py` using a fake GitHub CLI. It verifies refusals,
  uncertain merge results, accepted merges followed by lifecycle failure,
  independent dispatch and success. No real GitHub mutation is performed.
- The main dependency manifest and released checks are **not** repinned to
  the candidate; do not merge this candidate-only PR into main.

## Required gates

1. Get candidate-only PR CI green; report exact SHA and results to
   tool.cad.ci #110.
2. Fix any exposed defect in the tool repository, update candidate exact
   SHA and rerun.
3. Complete tool API/security/compatibility review before release.
4. After an immutable tool release, create a **separate released-stack
   acceptance PR**, update every pin, run all cases and only then approve
   Forge/CAD consumer adoption.

## Issue assessment

| Issue | Status | Next |
| --- | --- | --- |
| #86 Candidate contract qualification | **now** | Isolated candidate workflows and black-box fake API; no real mutation. |

Release-stability rules in `AGENTS.md` remain authoritative. This is an
isolated candidate qualification experiment, not a released-stack acceptance.

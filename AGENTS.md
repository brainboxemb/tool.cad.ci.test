# Repository instructions

## Purpose

`tool.cad.ci.test` is the permanent black-box acceptance repository for one
exact released `tool.cad.ci` + `lib.py.cad.ci` stack.

Keep it synthetic and domain-neutral. Do not add Forge, SolidCraft or real CAD
behaviour.

## Released-stack rule

The repository consumes only the exact tool commit in `dependencies.repos`.
That tool must itself pin one exact released library commit.

Never follow moving `main`.

Current accepted structure:

- `simple_case1`
- `more_complex_case2`
- `fresh_runner_case`
- `nested_item_case`
- `dependency_case`
- `active_dependents_case`
- `partial_rerun_case`
- `process_case`
- `directory_output_case`
- `timeout_case`
- `publish_case`
- `workflow_case`
- `merge_policy_case`

Each case owns a small `cad-ci.yml`, source files and `check.py`. A failure
must clearly identify the contract that broke.

## Development boundary

Do not develop generic CI behaviour here.

The sequence is:

1. define/design generic behaviour in `lib.py.cad.ci`;
2. implement, test and release the library;
3. pin that release in `tool.cad.ci`;
4. expose only the CLI adapter, test it and release the tool;
5. pin that exact tool release here;
6. prove the released stack with these cases;
7. only then migrate Forge or CAD.

If a case finds a generic gap, return to the library/tool. Do not add a local
workaround.

## Case helpers

`tests/support.py` may only provide process/file helpers such as:
- invoking the exact bootstrapped tool;
- copying a case to disposable output;
- deleting local SCons state for fresh-runner tests;
- reading JSON.

Do not put planner, SCons, cache, publication or domain decisions in the helper.

## Publication case

`publish_case` may use the real GitHub event and repository remote because its
purpose is to verify generated `build` and `gh-pages` branches.

It must use public `.cad-ci` evidence, never old custom fingerprint/state
files.

Source freshness failures, generated-branch publication and provenance are
tested through the released tool, not reimplemented in the case.

## Workflow

The workflow proves all released public consumption paths:
- direct CLI cases use the exact commit in `dependencies.repos`;
- `workflow_case` calls the single high-level `reusable-ci.yml` workflow from
  that same released commit and verifies its handed-off build output/evidence;
- `same_runner` consumes the root composite action from that exact released
  commit and proves a following step can reuse the exposed CLI stack on the
  same runner without another bootstrap.

Do not rebuild generic plan/run/cache orchestration in this repository. The
caller may provide domain-neutral inputs and inspect generic output/evidence,
but generic selection/execution semantics stay in the released tool/library
stack.

## Code and language

Use short literal engineering language and explanatory docstrings/comments for
non-obvious checks.

One logical acceptance update uses one issue, one branch and one pull request.

## Repository plan source of truth

`docs/plan.md` is the current source of truth for unfinished repository work.

Keep it as a current snapshot:

- state the current goal and execution order;
- include every open issue in an issue assessment snapshot;
- give each open issue an explicit status such as `now`, `later`, `blocked`, `probably obsolete`, or `effectively complete but still open`;
- explain briefly why that status applies;
- identify dependencies or blockers between issues;
- keep the issue assessment current when issues are opened, closed, merged or superseded.

Issues contain detail and history. README and design/requirements documents describe stable purpose and behavior. The plan tells an agent what work is actually current and what should happen next.



## Acceptance run policy

The complete external suite is automatic on pull requests only.
`workflow_dispatch` is the explicit main/manual rerun path.

Generated build/Pages publication tests use only an isolated local Git remote.
Do not reintroduce writes to this repository's real `build` or `gh-pages`
branches merely to test publication behavior.

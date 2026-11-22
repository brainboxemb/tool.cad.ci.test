# tool.cad.ci.test

Permanent black-box acceptance repository for the released generic CAD CI stack.

This repository currently pins:

- `tool.cad.ci` **0.18.1** at
  `e29d3127d5d3f9310f3cab4e27430a64a61c21cc`;
- that tool pins `lib.py.cad.ci` **0.11.0** at
  `e621daf6e309bdd0e3f643a12007f1b66490696d`;

No Forge, SolidCraft or real CAD behaviour belongs here. Each top-level case is
a small independent consumer repository that exercises the released tool from
the outside.

## Cases

```text
simple_case1/
more_complex_case2/
fresh_runner_case/
nested_item_case/
nested_publish_case/
dependency_case/
active_dependents_case/
partial_rerun_case/
process_case/
directory_output_case/
timeout_case/
publish_case/
workflow_case/
```

`simple_case1` proves cold build, unchanged CURRENT results, verify-only
invalidation and step-input membership changes.

`more_complex_case2` proves coarse Git changed-item selection separately from
SCons target freshness.

`fresh_runner_case` proves the hosted-runner path against exact Git base/head
revisions from a new clone with no build output or SCons cache: changing only
item A executes only A and leaves independent sibling B untouched.

`nested_item_case` proves root item templates, item-root-relative watch/input
paths, safe parent-relative item inputs and path-derived nested IDs together.
A child-source change selects one sibling; a shared parent-contract change
selects both children, each time from a fresh Git clone without build/cache.

`nested_publish_case` proves durable ownership for a parent item and nested
child item. Complete/sparse scopes can contain both, while parent-only and
child-only main updates preserve the unselected neighbor's output and evidence.

`dependency_case` proves cumulative dependency output, fan-out and
`affected: direct` summary behaviour.

`active_dependents_case` proves released `selection_context: direct_dependents`
from the outside: one selected consumer, signature invalidation for a different
consumer set, jobs=2 fan-out, full-run context and schema-5 public evidence.

`partial_rerun_case` proves the released meanings of exact `--step`,
`--until` and `--from`, including complete-item evidence after partial runs.

`process_case` proves omitted and explicit `process: true` items participate in
normal full planning/execution, while `process: false` is excluded and rejects
explicit execution.

`directory_output_case` proves complete directory output, empty directories,
local repair and fresh-runner CacheDir restore.

`timeout_case` distinguishes repository-default timeout, per-step timeout
override and ordinary command failure.

`publish_case` proves complete main output, sparse PR output, resolved views,
real generated `build` branch publication, Pages stable/preview publication
and source/build provenance.

`workflow_case` is the root consumer used by GitHub itself. It proves the
released high-level `reusable-ci.yml` workflow from another repository. The
caller supplies `ACCEPTANCE_MARKER=reusable-workflow`, while root
`cad-ci.yml` declares `ACCEPTANCE_MARKER=repository-config`. The consumer
must observe the repository value, proving root repository variables reach the
command and override the inherited caller value.

The same real consumer command also checks that Docker already contains a
`ghcr.io` authentication entry. It checks only the registry-key presence and
never reads, decodes or writes the credential value. This proves the released reusable workflow performs generic GHCR login before
consumer CAD-CI commands.

The downstream job also verifies generated output, item evidence and step
evidence with public `output_state` terminology.

## How it runs

`dependencies.repos` stores one exact tool commit for the CLI acceptance cases.
`scripts/bootstrap.py` checks that commit out under `ext/cad-ci`.
The workflow calls the high-level `reusable-ci.yml` and the root composite
action from that exact released commit. The reusable workflow path still
uploads its generated `build/` tree for a downstream acceptance job. The
same-runner action path deliberately keeps its generated `build/` tree and
exact CLI source stack in the caller job instead of transporting them.

Most cases copy their immutable template to `output/cases/<name>` before
mutating inputs. The publication case runs against its own source tree because
it also verifies the real GitHub event source SHA and generated branches.

## Boundary

If a case exposes missing generic behaviour, the implementation belongs in
`lib.py.cad.ci` first, followed by a released `tool.cad.ci`. Do not patch
around missing generic behaviour in this repository.

External package/image lookup is not a public `tool.cad.ci` command.
The Forge GHCR image-existence problem is therefore not implemented or faked in
this acceptance repository.

Forge and CAD may update their tool pin only after this exact released stack is
green here.


## Same-runner action acceptance

The `same_runner` job consumes
`brainboxemb/tool.cad.ci@e29d3127d5d3f9310f3cab4e27430a64a61c21cc` directly as a composite action.

The action runs the real root `workflow_case`. The immediately following step
does not bootstrap CAD-CI again. It verifies that:

- `cad_ci_tool` imports from `CAD_CI_TOOL_ROOT`;
- `cad_ci` imports from `CAD_CI_LIB_ROOT`;
- the action reports the exact pinned library commit;
- `python -m cad_ci_tool plan` works on the same runner;
- the action-produced build output and public evidence are still present.

This same-runner proof remains part of the complete external acceptance gate
for every exact released tool/library pair before Forge or CAD adopts it.

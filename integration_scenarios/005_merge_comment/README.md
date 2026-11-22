# 005 merge comment

Status: current

## Purpose

Prove the actual GitHub `issue_comment` entrypoint of the released merge
policy.

## Real execution

On a green eligible lane PR, the repository owner posts exactly:

```text
/merge
```

## Acceptance

A real `issue_comment` Actions event must invoke
`reusable-merge-policy.yml@v0.25.0`.

The released policy, not local shell/YAML logic, must:

- validate the PR relationship;
- choose the merge behavior;
- perform the merge;
- preserve permanent branches where required;
- dispatch the configured post-merge integration workflow.

Mock/fake-GitHub tests may supplement owner-unit coverage but do not replace
this live scenario.

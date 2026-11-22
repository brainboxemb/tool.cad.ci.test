"""Black-box source contract for released tool.cad.ci merge policy."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "ext" / "cad-ci"
POLICY = TOOL / "scripts" / "merge_policy.py"
WORKFLOW = TOOL / ".github" / "workflows" / "reusable-merge-policy.yml"
EXPECTED_TOOL = "5677c41a61929b32ab2cb07087a6505f7b9347d8"
EXPECTED_LIBRARY = "e621daf6e309bdd0e3f643a12007f1b66490696d"


def load_policy():
    """Load the helper only from the exact bootstrapped released tool source."""

    spec = importlib.util.spec_from_file_location(
        "released_merge_policy",
        POLICY,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load released merge-policy helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Fail unless released 0.19.0 exposes the intended generic contract."""

    version = (TOOL / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.19.0":
        raise RuntimeError(f"unexpected tool release: {version}")

    dependency = (TOOL / "pyproject.toml").read_text(encoding="utf-8")
    if EXPECTED_LIBRARY not in dependency:
        raise RuntimeError("tool 0.19.0 does not pin accepted library 0.11.0")

    policy = load_policy()
    lanes = ("cad-work", "ci-work")
    permanent = ("build-output", "pages-output")

    for head in lanes:
        value = policy.evaluate(
            base="stable",
            head=head,
            stable_ref="stable",
            lane_refs=lanes,
            permanent_refs=permanent,
        )
        if value.merge_method != "merge" or not value.direct_lane_promotion:
            raise RuntimeError(f"lane promotion policy mismatch: {head}: {value}")
        if value.cleanup_head:
            raise RuntimeError(f"long-lived lane became cleanup eligible: {head}")

    feature = policy.evaluate(
        base="cad-work",
        head="feature/example",
        stable_ref="stable",
        lane_refs=lanes,
        permanent_refs=permanent,
    )
    if feature.merge_method != "squash":
        raise RuntimeError(f"short-lived merge is not squash: {feature}")
    if not feature.cleanup_head:
        raise RuntimeError(f"allow-listed temporary head is not cleanup eligible: {feature}")

    for head in (
        "stable",
        "cad-work",
        "ci-work",
        "build-output",
        "pages-output",
        "backup/stable-before-change",
        "release/1.0",
        "unknown",
    ):
        if policy.is_cleanup_eligible(
            head,
            stable_ref="stable",
            lane_refs=lanes,
            permanent_refs=permanent,
            temporary_prefixes=("issue/", "feature/"),
        ):
            raise RuntimeError(f"protected/unknown ref became cleanup eligible: {head}")

    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        "workflow_call:",
        "inputs.command == '/merge'",
        "github.actor == github.repository_owner",
        "check-runs?per_page=100",
        "group_by(.name)",
        'sha="$HEAD_SHA"',
        'merge_method="$METHOD"',
        "job.workflow_repository",
        "job.workflow_sha",
        "scripts/merge_policy.py",
        "long-lived lane recreated at merge commit",
        "temporary head deleted",
        "INTEGRATION_WORKFLOW",
    )
    for value in required:
        if value not in text:
            raise RuntimeError(f"released merge workflow missing contract: {value}")

    forbidden = (
        "dev-cad",
        "dev-ci",
        "scpf.yml",
        "lib.py.solidcraft.forge",
    )
    for value in forbidden:
        if value in text:
            raise RuntimeError(f"consumer-specific value leaked into workflow: {value}")

    inputs = text.split("inputs:", 1)[1].split("permissions:", 1)[0]
    if "merge_method:" in inputs:
        raise RuntimeError("caller can choose arbitrary merge method")

    # The released workflow is intentionally mutation-capable. This acceptance
    # case proves its exact decision/safety surface without creating a synthetic
    # GitHub PR or ref. Forge #674 performs the real success-path mutation proof.
    print(
        "released tool 0.19.0 merge-policy contract accepted; "
        f"tool={EXPECTED_TOOL} library={EXPECTED_LIBRARY}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Black-box source contract for released tool.cad.ci merge policy."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "ext" / "cad-ci"
POLICY = TOOL / "scripts" / "merge_policy.py"
WORKFLOW = TOOL / ".github" / "workflows" / "reusable-merge-policy.yml"
EXPECTED_TOOL = "eb64a46b243db00e8dbb4b78b6643a2a7efa3fb9"
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
    """Fail unless released 0.20.1 exposes the intended generic contract."""

    version = (TOOL / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.20.1":
        raise RuntimeError(f"unexpected tool release: {version}")

    dependency = (TOOL / "pyproject.toml").read_text(encoding="utf-8")
    if EXPECTED_LIBRARY not in dependency:
        raise RuntimeError("tool 0.20.1 does not pin accepted library 0.11.0")

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
        if value.direct_lane_synchronization:
            raise RuntimeError(f"lane promotion misclassified as synchronization: {head}: {value}")
        if value.cleanup_head:
            raise RuntimeError(f"long-lived lane became cleanup eligible: {head}")

    for base in lanes:
        value = policy.evaluate(
            base=base,
            head="stable",
            stable_ref="stable",
            lane_refs=lanes,
            permanent_refs=permanent,
        )
        if value.merge_method != "merge" or not value.direct_lane_synchronization:
            raise RuntimeError(f"stable-to-lane policy mismatch: {base}: {value}")
        if value.direct_lane_promotion:
            raise RuntimeError(f"lane synchronization misclassified as promotion: {base}: {value}")
        if value.cleanup_head:
            raise RuntimeError(f"stable ref became cleanup eligible during sync: {base}: {value}")
        if not value.integrate_base:
            raise RuntimeError(f"synchronized lane did not request integration: {base}: {value}")

    lane_to_lane = policy.evaluate(
        base="cad-work",
        head="ci-work",
        stable_ref="stable",
        lane_refs=lanes,
        permanent_refs=permanent,
    )
    if lane_to_lane.merge_method != "squash":
        raise RuntimeError(f"lane-to-lane merge is not squash: {lane_to_lane}")
    if lane_to_lane.direct_lane_promotion or lane_to_lane.direct_lane_synchronization:
        raise RuntimeError(f"lane-to-lane merge became permanent-direction operation: {lane_to_lane}")
    if lane_to_lane.cleanup_head:
        raise RuntimeError(f"permanent lane head became cleanup eligible: {lane_to_lane}")

    feature = policy.evaluate(
        base="cad-work",
        head="feature/example",
        stable_ref="stable",
        lane_refs=lanes,
        permanent_refs=permanent,
    )
    if feature.merge_method != "squash":
        raise RuntimeError(f"short-lived merge is not squash: {feature}")
    if feature.direct_lane_promotion or feature.direct_lane_synchronization:
        raise RuntimeError(f"short-lived merge became permanent-direction operation: {feature}")
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
        "event=issue_comment",
        "COMMAND_RUN_IDS",
        ".details_url",
        "/actions/runs/",
        "group_by(.name)",
        'sha="$HEAD_SHA"',
        'merge_method="$METHOD"',
        "job.workflow_repository",
        "job.workflow_sha",
        "scripts/merge_policy.py",
        "long-lived lane recreated at merge commit",
        "long-lived lane synchronized by merge",
        "DIRECT_SYNC",
        "long-lived permanent merge must originate from this repository",
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
    # GitHub PR or ref. Forge #721 performs the real same-head command and
    # stable-to-lane mutation proof after this release is adopted.
    print(
        "released tool 0.20.1 merge-policy contract accepted; "
        f"tool={EXPECTED_TOOL} library={EXPECTED_LIBRARY}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Black-box source contract for released tool.cad.ci merge policy."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import TOOL_ROOT


POLICY = TOOL_ROOT / "scripts" / "merge_policy.py"
WORKFLOW = TOOL_ROOT / ".github" / "workflows" / "reusable-merge-policy.yml"
EXPECTED_VERSION = "0.27.1"
EXPECTED_LIBRARY = "64656db8df528a5c0de799e62c0f028fd0133486"


def load_policy():
    """Load the helper only from the released tool source used by this run."""

    spec = importlib.util.spec_from_file_location("released_merge_policy", POLICY)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load released merge-policy helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Fail unless the loaded release exposes the intended generic contract."""

    version = (TOOL_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != EXPECTED_VERSION:
        raise RuntimeError(f"unexpected tool release: {version}")

    dependency = (TOOL_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if EXPECTED_LIBRARY not in dependency:
        raise RuntimeError("tool does not pin accepted library 0.12.0")

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
        if value.direct_lane_synchronization or value.cleanup_head:
            raise RuntimeError(f"lane promotion safety mismatch: {head}: {value}")

    for base in lanes:
        value = policy.evaluate(
            base=base,
            head="stable",
            stable_ref="stable",
            lane_refs=lanes,
            permanent_refs=permanent,
        )
        if value.merge_method != "merge" or not value.direct_lane_synchronization:
            raise RuntimeError(f"lane synchronization mismatch: {base}: {value}")
        if value.direct_lane_promotion or value.cleanup_head or not value.integrate_base:
            raise RuntimeError(f"lane synchronization safety mismatch: {base}: {value}")

    feature = policy.evaluate(
        base="cad-work",
        head="feature/example",
        stable_ref="stable",
        lane_refs=lanes,
        permanent_refs=permanent,
    )
    if feature.merge_method != "squash" or not feature.cleanup_head:
        raise RuntimeError(f"temporary merge policy mismatch: {feature}")

    text = WORKFLOW.read_text(encoding="utf-8")
    for value in (
        "workflow_call:",
        "inputs.command == '/merge'",
        "github.actor == github.repository_owner",
        "job.workflow_repository",
        "job.workflow_sha",
        "scripts/merge_command.py",
        "persist-credentials: false",
    ):
        if value not in text:
            raise RuntimeError(f"released merge workflow missing contract: {value}")

    if "gh api" in text:
        raise RuntimeError("GitHub API mutation logic leaked into workflow YAML")

    print(
        "released merge-policy contract accepted; "
        f"tool={EXPECTED_VERSION} library={EXPECTED_LIBRARY}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

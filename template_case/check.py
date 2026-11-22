"""Black-box acceptance for released tool.cad.ci consumer templates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "ext" / "cad-ci"
TEMPLATES = TOOL / "templates"
MARKER = "TOOL_CAD_CI_RELEASE_SHA"


def main() -> None:
    manifest = json.loads(
        (TEMPLATES / "manifest.json").read_text(encoding="utf-8")
    )
    if manifest.get("schema") != 1:
        raise SystemExit(f"unexpected template manifest schema: {manifest}")

    expected = {
        "github/workflows/cad-ci.yml":
            ("tool.cad.ci/cad-ci", 1, "reusable-ci.yml"),
        "github/workflows/cad-ci-pr.yml":
            ("tool.cad.ci/cad-ci-pr", 1, "reusable-pr.yml"),
        "github/workflows/cad-ci-same-runner.yml":
            ("tool.cad.ci/cad-ci-same-runner", 1, "action.yml"),
        "github/workflows/merge-policy.yml":
            ("tool.cad.ci/merge-policy", 1, "reusable-merge-policy.yml"),
    }
    if set(manifest.get("templates", {})) != set(expected):
        raise SystemExit(f"unexpected released template set: {manifest}")

    forbidden = (
        "actions/checkout@",
        "actions/setup-python@",
        "gh api",
        "pip install",
        "docker login",
        "scripts/reusable_ci.py",
        "cad-ci run",
        "forge",
        "solidcraft",
        "2026-011-02",
        "cad.yml",
    )

    for relative, (template_id, version, surface) in expected.items():
        path = TEMPLATES / relative
        text = path.read_text(encoding="utf-8")
        entry = manifest["templates"][relative]
        if entry != {
            "id": template_id,
            "version": version,
            "surface": surface,
        }:
            raise SystemExit(f"manifest mismatch for {relative}: {entry}")
        if f"# template: {template_id}" not in text:
            raise SystemExit(f"missing template id in {relative}")
        if f"# template-version: {version}" not in text:
            raise SystemExit(f"missing template version in {relative}")
        if text.count(MARKER) != 2:
            raise SystemExit(
                f"{relative} must contain marker in instruction + public call"
            )
        lowered = text.lower()
        leaked = [value for value in forbidden if value in lowered]
        if leaked:
            raise SystemExit(
                f"generic/consumer implementation leaked into {relative}: {leaked}"
            )

    guide = (TOOL / "docs" / "new-repository.md").read_text(encoding="utf-8")
    for value in (
        "templates/github/workflows/",
        "TOOL_CAD_CI_RELEASE_SHA",
        "template-version",
        "Never consume moving",
    ):
        if value not in guide:
            raise SystemExit(f"released onboarding missing: {value}")

    print("released tool.cad.ci 0.22.0 consumer templates accepted")


if __name__ == "__main__":
    main()

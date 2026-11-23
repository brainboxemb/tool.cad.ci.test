#!/usr/bin/env python3
"""Render black-box evidence for the post-build Pages publication boundary."""

from __future__ import annotations

import html
import json
import os
from pathlib import Path


REQUIRED = (
    "CAD_CI_REPO",
    "CAD_CI_OUTPUT",
    "CAD_CI_BUILDER",
    "CAD_CI_BUILDER_PATH",
    "CAD_CI_COMPLETE_SCOPE",
    "CAD_CI_BUILD_SCOPE",
    "CAD_CI_SOURCE_SHA",
    "CAD_CI_SOURCE_REF",
    "CAD_CI_BUILD_COMMIT",
    "ACCEPTANCE_MARKER",
)


def main() -> int:
    values = {name: os.environ.get(name, "").strip() for name in REQUIRED}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(
            "missing publication environment: " + ", ".join(missing)
        )
    if values["CAD_CI_BUILDER"] != "acceptance-pages":
        raise RuntimeError("unexpected publication builder")
    if values["ACCEPTANCE_MARKER"] != "repository-config":
        raise RuntimeError("repository variable did not override caller value")

    complete = Path(values["CAD_CI_COMPLETE_SCOPE"]).resolve()
    manifest_path = complete / "build.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"missing complete-scope build manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("source_commit") != values["CAD_CI_SOURCE_SHA"]:
        raise RuntimeError("complete-scope source commit does not match renderer source")
    if manifest.get("scope") != values["CAD_CI_BUILD_SCOPE"]:
        raise RuntimeError("complete-scope manifest scope does not match renderer scope")
    rows = manifest.get("items")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("complete-scope manifest has no item rows")
    acceptance = next(
        (row for row in rows if row.get("id") == "acceptance-suite"),
        None,
    )
    if acceptance is None:
        raise RuntimeError("complete-scope manifest lacks acceptance-suite evidence")

    output = Path(values["CAD_CI_OUTPUT"]).resolve()
    site = output / "site"
    site.mkdir(parents=True, exist_ok=True)

    evidence = {
        "schema": 1,
        "builder": values["CAD_CI_BUILDER"],
        "builder_path": values["CAD_CI_BUILDER_PATH"],
        "complete_scope": values["CAD_CI_COMPLETE_SCOPE"],
        "build_scope": values["CAD_CI_BUILD_SCOPE"],
        "source_sha": values["CAD_CI_SOURCE_SHA"],
        "source_ref": values["CAD_CI_SOURCE_REF"],
        "build_commit": values["CAD_CI_BUILD_COMMIT"],
        "acceptance_marker": values["ACCEPTANCE_MARKER"],
        "manifest": {
            "schema": manifest.get("schema"),
            "scope": manifest.get("scope"),
            "source_commit": manifest.get("source_commit"),
            "acceptance_suite_source_commit": acceptance.get("source_commit"),
            "acceptance_suite_final_step": acceptance.get("final_step"),
        },
    }
    (site / "context.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (site / "index.html").write_text(
        "<!doctype html><title>tool.cad.ci.test</title>"
        "<h1>post-build Pages renderer</h1>"
        f"<p>scope={html.escape(values['CAD_CI_BUILD_SCOPE'])}</p>"
        f"<p>source={html.escape(values['CAD_CI_SOURCE_SHA'])}</p>"
        f"<p>build={html.escape(values['CAD_CI_BUILD_COMMIT'])}</p>\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

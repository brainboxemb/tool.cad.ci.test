#!/usr/bin/env python3
"""Black-box synthetic durable workflow consumer acceptance."""

from __future__ import annotations

from pathlib import Path
import json
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, read_json, run_tool


CASE = Path(__file__).resolve().parent
SHA_MAIN = "1" * 40
SHA_NAMED = "2" * 40


def publication_site(
    source: Path,
    target: Path,
    *,
    source_commit: str,
    build_commit: str,
    build_scope: str,
) -> Path:
    """Create valid public Pages input without changing builder output."""

    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target)
    (target / "provenance.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "source_commit": source_commit,
                "build_commit": build_commit,
                "build_scope": build_scope,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return target


def main() -> int:
    repo = fresh_case(CASE, "016_durable_workflow")
    run_tool("run", "--repo", str(repo))

    assert (repo / "build/items/normal/result.txt").read_text() == "normal\n"
    site = repo / "build/items/site/site/index.html"
    assert "synthetic durable site" in site.read_text(encoding="utf-8")

    out = ROOT / "output" / "016_durable_workflow"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    stable = out / "stable"
    run_tool(
        "build",
        "prepare-main",
        "--repo",
        str(repo),
        "--candidate-root",
        str(repo / "build"),
        "--out",
        str(stable),
        "--source-commit",
        SHA_MAIN,
    )
    stable_manifest = read_json(stable / "build.json")
    assert stable_manifest["scope"] == "main"
    assert stable_manifest["source_commit"] == SHA_MAIN
    assert (stable / "items/normal/result.txt").read_text() == "normal\n"
    assert (stable / "items/site/site/index.html").is_file()

    pages = out / "pages"
    stable_site = publication_site(
        stable / "items/site/site",
        out / "stable-site",
        source_commit=SHA_MAIN,
        build_commit="3" * 40,
        build_scope="main",
    )
    run_tool(
        "pages",
        "install-stable",
        "--site",
        str(stable_site),
        "--pages-root",
        str(pages),
    )
    stable_html = (pages / "index.html").read_bytes()

    named = out / "named"
    run_tool(
        "build",
        "prepare-named",
        "--repo",
        str(repo),
        "--candidate-root",
        str(repo / "build"),
        "--out",
        str(named),
        "--source-commit",
        SHA_NAMED,
        "--name",
        "dev-ci",
    )
    named_manifest = read_json(named / "build.json")
    assert named_manifest["scope"] == "named"
    assert named_manifest["name"] == "dev-ci"
    assert named_manifest["source_commit"] == SHA_NAMED

    named_site = publication_site(
        named / "items/site/site",
        out / "named-site",
        source_commit=SHA_NAMED,
        build_commit="4" * 40,
        build_scope="dev-ci",
    )
    run_tool(
        "pages",
        "install-named",
        "--site",
        str(named_site),
        "--pages-root",
        str(pages),
        "--name",
        "dev-ci",
    )
    assert (pages / "index.html").read_bytes() == stable_html
    assert (pages / "dev-ci/index.html").is_file()

    print("test_roots/016_durable_workflow passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

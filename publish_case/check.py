#!/usr/bin/env python3
"""Black-box durable build and real generated-branch publication acceptance."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import read_json, run_tool

CASE = Path(__file__).resolve().parent


def git(*args: str) -> str:
    """Run Git in the actual test repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def git_in(repo: Path, *args: str) -> str:
    """Run Git in one explicit repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def isolated_repository(
    out: Path,
    source_sha: str,
    source_ref: str,
) -> Path:
    """Create a local remote/clone pair for real publication commands."""

    remote = out / "remote.git"
    repository = out / "repository"
    shutil.rmtree(remote, ignore_errors=True)
    shutil.rmtree(repository, ignore_errors=True)

    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(remote)],
        check=True,
    )
    # The normal reusable workflow intentionally checks out only the exact
    # source commit. This local fixture accepts that shallow commit without
    # forcing an unrelated history fetch into the consumer workflow.
    subprocess.run(
        [
            "git",
            "--git-dir",
            str(remote),
            "config",
            "receive.shallowUpdate",
            "true",
        ],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "push",
            "--quiet",
            str(remote),
            f"{source_sha}:refs/heads/{source_ref}",
        ],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "--git-dir",
            str(remote),
            "symbolic-ref",
            "HEAD",
            f"refs/heads/{source_ref}",
        ],
        check=True,
    )
    subprocess.run(
        ["git", "clone", "--quiet", str(remote), str(repository)],
        check=True,
    )
    git_in(repository, "config", "user.name", "tool.cad.ci.test")
    git_in(
        repository,
        "config",
        "user.email",
        "tool.cad.ci.test@example.invalid",
    )
    if git_in(repository, "rev-parse", "HEAD") != source_sha:
        raise RuntimeError("isolated repository is not at the event source commit")
    return repository


def source_event() -> tuple[str, str, str, int]:
    """Return event name, source SHA/ref and PR number."""

    event_name = os.environ["GITHUB_EVENT_NAME"]
    event = json.loads(
        Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")
    )
    if event_name == "pull_request":
        pull_request = event["pull_request"]
        return (
            event_name,
            pull_request["head"]["sha"],
            pull_request["head"]["ref"],
            int(event["number"]),
        )
    return (
        event_name,
        os.environ["GITHUB_SHA"],
        os.environ["GITHUB_REF_NAME"],
        0,
    )


def build_site(path: Path, source_sha: str, build_commit: str) -> None:
    """Write the minimal site required by the generic Pages publisher."""

    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)
    (path / "index.html").write_text(
        "<!doctype html><title>tool.cad.ci.test</title>"
        "<p>publication acceptance passed</p>\n",
        encoding="utf-8",
    )
    (path / "provenance.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "source_commit": source_sha,
                "build_commit": build_commit,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def assert_item_evidence(path: Path, expected_item: str) -> None:
    """Check the public evidence format in fetched durable output."""

    state = read_json(path)
    assert state["schema"] == 2
    assert state["engine"] == "scons"
    assert state["status"] == "pass"
    assert state["item"] == expected_item
    assert state["final_bundle_sha256"]
    assert state["run_started_at"]
    assert state["run_finished_at"]


def local_build_store_checks(out: Path, source_sha: str) -> None:
    """Prove complete main, sparse overlay and resolved view locally."""

    local_main = out / "local-main"
    run_tool(
        "build",
        "prepare-main",
        "--repo",
        str(CASE),
        "--candidate-root",
        str(CASE / "build"),
        "--out",
        str(local_main),
        "--source-commit",
        source_sha,
    )
    assert (local_main / "items/a/.cad-ci/item.json").is_file()
    assert (local_main / "items/b/.cad-ci/item.json").is_file()

    overlay = out / "local-overlay"
    run_tool(
        "build",
        "prepare-pr",
        "--repo",
        str(CASE),
        "--candidate-root",
        str(CASE / "build"),
        "--out",
        str(overlay),
        "--source-commit",
        source_sha,
        "--pull-request",
        "999999",
        "--items",
        "publish-a",
    )
    assert (overlay / "items/a/.cad-ci/item.json").is_file()
    assert not (overlay / "items/b").exists()

    resolved = out / "local-resolved"
    run_tool(
        "build",
        "resolve",
        "--main",
        str(local_main),
        "--overlay",
        str(overlay),
        "--out",
        str(resolved),
    )
    assert (resolved / "items/a/result.txt").read_text() == "a\n"
    assert (resolved / "items/b/result.txt").read_text() == "b\n"

    removed_item_build_store_checks(out, source_sha, local_main)


def removed_item_build_store_checks(
    out: Path,
    source_sha: str,
    local_main: Path,
) -> None:
    """Prove removed durable items through the released update-main CLI."""

    current_repo = out / "removed-item-current"
    shutil.copytree(
        CASE,
        current_repo,
        ignore=shutil.ignore_patterns(
            "build",
            ".cache",
            "__pycache__",
        ),
    )
    shutil.rmtree(current_repo / "items" / "b")

    a_result_before = (
        local_main / "items/a/result.txt"
    ).read_bytes()
    a_evidence_before = (
        local_main / "items/a/.cad-ci/item.json"
    ).read_bytes()

    deletion_only = out / "removed-item-deletion-only"
    run_tool(
        "build",
        "update-main",
        "--repo",
        str(current_repo),
        "--candidate-root",
        str(CASE / "build"),
        "--main",
        str(local_main),
        "--out",
        str(deletion_only),
        "--source-commit",
        source_sha,
        "--changed",
        "items/b/ci.yml",
    )
    assert (
        deletion_only / "items/a/result.txt"
    ).read_bytes() == a_result_before
    assert (
        deletion_only / "items/a/.cad-ci/item.json"
    ).read_bytes() == a_evidence_before
    assert not (deletion_only / "items/b").exists()
    deletion_manifest = read_json(deletion_only / "build.json")
    assert tuple(deletion_manifest["items"]) == ("items/a",)

    mixed = out / "removed-item-mixed"
    run_tool(
        "build",
        "update-main",
        "--repo",
        str(current_repo),
        "--candidate-root",
        str(CASE / "build"),
        "--main",
        str(local_main),
        "--out",
        str(mixed),
        "--source-commit",
        source_sha,
        "--changed",
        "items/a/run.py",
    )
    assert (mixed / "items/a/result.txt").read_text() == "a\n"
    assert not (mixed / "items/b").exists()
    mixed_manifest = read_json(mixed / "build.json")
    assert tuple(mixed_manifest["items"]) == ("items/a",)
    assert (
        mixed_manifest["items"]["items/a"]["source_commit"]
        == source_sha
    )


def named_scope_publication_checks(
    out: Path,
    repository: Path,
    source_sha: str,
    source_ref: str,
) -> None:
    """Prove released named build/Page scopes preserve every sibling."""

    def prepare_scope(name: str | None, stamp: str) -> Path:
        candidate = out / f"scope-{stamp}"
        args = [
            "build",
            "prepare-main" if name is None else "prepare-named",
            "--repo",
            str(CASE),
            "--candidate-root",
            str(CASE / "build"),
            "--out",
            str(candidate),
            "--source-commit",
            stamp,
        ]
        if name is not None:
            args.extend(["--name", name])
        run_tool(*args)
        return candidate

    def publish_scope(name: str | None, stamp: str) -> str:
        candidate = prepare_scope(name, stamp)
        args = [
            "publish",
            "build",
            "--repo",
            str(repository),
            "--candidate",
            str(candidate),
            "--scope",
            "main" if name is None else "named",
            "--message",
            f"publish {stamp}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ]
        if name is not None:
            args.extend(["--scope-name", name])
        return run_tool(*args).strip()

    publish_scope(None, "stable-build-1")
    publish_scope("dev_a", "dev-a-build-1")
    publish_scope("dev_b", "dev-b-build-1")
    publish_scope("dev_a", "dev-a-build-2")

    generated = out / "named-generated-build"
    run_tool(
        "build",
        "fetch",
        "--repo",
        str(repository),
        "--out",
        str(generated),
    )
    assert read_json(generated / "main/build.json")["source_commit"] == "stable-build-1"
    assert read_json(generated / "dev_a/build.json")["source_commit"] == "dev-a-build-2"
    assert read_json(generated / "dev_b/build.json")["source_commit"] == "dev-b-build-1"

    def publish_site(
        label: str,
        *,
        name: str | None = None,
        preserve: tuple[str, ...] = (),
    ) -> None:
        site = out / f"site-{label}"
        build_site(site, label, f"build-{label}")
        args = [
            "publish",
            "pages",
            "--repo",
            str(repository),
            "--site",
            str(site),
            "--message",
            f"pages {label}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ]
        if name is not None:
            args.extend(["--name", name])
        for subtree in preserve:
            args.extend(["--preserve-subtree", subtree])
        run_tool(*args)

    publish_site("stable-page-1")
    publish_site("dev-a-page-1", name="dev_a")
    publish_site("dev-b-page-1", name="dev_b")
    publish_site("dev-a-page-2", name="dev_a")
    publish_site(
        "stable-page-2",
        preserve=("dev_a", "dev_b"),
    )

    git_in(repository, "fetch", "--quiet", "origin", "gh-pages")
    stable = json.loads(
        git_in(repository, "show", "origin/gh-pages:provenance.json")
    )
    dev_a = json.loads(
        git_in(repository, "show", "origin/gh-pages:dev_a/provenance.json")
    )
    dev_b = json.loads(
        git_in(repository, "show", "origin/gh-pages:dev_b/provenance.json")
    )
    assert stable["source_commit"] == "stable-page-2"
    assert dev_a["source_commit"] == "dev-a-page-2"
    assert dev_b["source_commit"] == "dev-b-page-1"

    unsafe = run_tool(
        "publish",
        "pages",
        "--repo",
        str(repository),
        "--site",
        str(out / "site-dev-a-page-2"),
        "--name",
        "../escape",
        "--message",
        "reject unsafe subtree",
        "--source-ref",
        source_ref,
        "--expected-source",
        source_sha,
        expect=2,
    )
    assert "unsafe" in unsafe.lower()


def main() -> int:
    event_name, source_sha, source_ref, pull_request = source_event()
    if git("rev-parse", "HEAD") != source_sha:
        raise RuntimeError("workflow checkout is not the event source commit")

    # Build the immutable case in place; generated output is ignored by Git.
    shutil.rmtree(CASE / "build", ignore_errors=True)
    shutil.rmtree(CASE / ".cache", ignore_errors=True)
    run_tool("run", "--repo", str(CASE))

    out = ROOT / "output" / "publish_case"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    local_build_store_checks(out, source_sha)
    repository = isolated_repository(out, source_sha, source_ref)

    # Source freshness is a safety boundary. A deliberately wrong expected
    # source SHA must be rejected before any generated branch is changed.
    stale_site = out / "stale-site"
    build_site(stale_site, source_sha, "not-published")
    stale = run_tool(
        "publish",
        "pages",
        "--repo",
        str(repository),
        "--site",
        str(stale_site),
        "--message",
        "This publication must be rejected",
        "--source-ref",
        source_ref,
        "--expected-source",
        "0" * 40,
        expect=2,
    )
    assert "moved" in stale or "expected" in stale

    named_scope_publication_checks(
        out,
        repository,
        source_sha,
        source_ref,
    )

    if event_name == "pull_request":
        candidate = out / "pr"
        run_tool(
            "build",
            "prepare-pr",
            "--repo",
            str(CASE),
            "--candidate-root",
            str(CASE / "build"),
            "--out",
            str(candidate),
            "--source-commit",
            source_sha,
            "--pull-request",
            str(pull_request),
            "--items",
            "publish-a",
        )
        build_commit = run_tool(
            "publish",
            "build",
            "--repo",
            str(repository),
            "--candidate",
            str(candidate),
            "--scope",
            "pr",
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish tool.cad.ci.test PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ).strip()

        site = out / "site"
        build_site(site, source_sha, build_commit)
        run_tool(
            "publish",
            "pages",
            "--repo",
            str(repository),
            "--site",
            str(site),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish tool.cad.ci.test preview PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        generated = out / "generated-build"
        fetched = run_tool(
            "build",
            "fetch",
            "--repo",
            str(repository),
            "--out",
            str(generated),
        ).strip()
        assert fetched == build_commit
        evidence = (
            generated
            / f"pr/{pull_request}/items/a/.cad-ci/item.json"
        )
        assert_item_evidence(evidence, "publish-a")
        assert not (
            generated / f"pr/{pull_request}/items/b"
        ).exists()

        git_in(repository, "fetch", "--quiet", "origin", "gh-pages")
        preview = json.loads(
            git_in(
                repository,
                "show",
                f"origin/gh-pages:previews/pr-{pull_request}/provenance.json",
            )
        )
        assert preview["source_commit"] == source_sha
        assert preview["build_commit"] == build_commit

        run_tool(
            "publish",
            "build-cleanup",
            "--repo",
            str(repository),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Clean tool.cad.ci.test PR #{pull_request} build",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )
        run_tool(
            "publish",
            "pages-cleanup",
            "--repo",
            str(repository),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Clean tool.cad.ci.test PR #{pull_request} preview",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        cleaned = out / "generated-build-cleaned"
        run_tool(
            "build",
            "fetch",
            "--repo",
            str(repository),
            "--out",
            str(cleaned),
        )
        assert not (cleaned / f"pr/{pull_request}").exists()

        git_in(repository, "fetch", "--quiet", "origin", "gh-pages")
        preview_check = subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"origin/gh-pages:previews/pr-{pull_request}/provenance.json",
            ],
            cwd=repository,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert preview_check.returncode != 0
    else:
        candidate = out / "main"
        run_tool(
            "build",
            "prepare-main",
            "--repo",
            str(CASE),
            "--candidate-root",
            str(CASE / "build"),
            "--out",
            str(candidate),
            "--source-commit",
            source_sha,
        )
        build_commit = run_tool(
            "publish",
            "build",
            "--repo",
            str(repository),
            "--candidate",
            str(candidate),
            "--scope",
            "main",
            "--message",
            f"Publish tool.cad.ci.test main {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ).strip()

        site = out / "site"
        build_site(site, source_sha, build_commit)
        run_tool(
            "publish",
            "pages",
            "--repo",
            str(repository),
            "--site",
            str(site),
            "--message",
            f"Publish tool.cad.ci.test stable {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        generated = out / "generated-build"
        fetched = run_tool(
            "build",
            "fetch",
            "--repo",
            str(repository),
            "--out",
            str(generated),
        ).strip()
        assert fetched == build_commit
        assert_item_evidence(
            generated / "main/items/a/.cad-ci/item.json",
            "publish-a",
        )
        assert_item_evidence(
            generated / "main/items/b/.cad-ci/item.json",
            "publish-b",
        )

        git_in(repository, "fetch", "--quiet", "origin", "gh-pages")
        stable = json.loads(
            git_in(repository, "show", "origin/gh-pages:provenance.json")
        )
        assert stable["source_commit"] == source_sha
        assert stable["build_commit"] == build_commit

    print("publish_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

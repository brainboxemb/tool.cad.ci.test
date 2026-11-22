#!/usr/bin/env python3
"""Black-box released merge-command contract: execute the CLI with a fake GitHub API.

The fake 'gh' command writes only into a temporary directory. No live API
mutation is performed; real GitHub mutation acceptance is a separate gate.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "ext" / "cad-ci"
HEAD = "b" * 40
BASE = "a" * 40
MERGE = "c" * 40
GITHUB_STUB = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
if not args or args[0] != "api":
    raise SystemExit("only gh api is allowed")
args = args[1:]
method = args[args.index("-X") + 1]
endpoint = next(a for a in args if a.startswith("repos/"))
fields = {}
for idx, item in enumerate(args):
    if item in ("-f", "-F"):
        name, value = args[idx + 1].split("=", 1)
        fields[name] = value
scenario = os.environ["RELEASED_SCENARIO"]
head = "b" * 40
base = "a" * 40
merge = "c" * 40
with Path(os.environ["FAKE_GH_CALLS"]).open("a", encoding="utf-8") as out:
    out.write(json.dumps({"method": method, "endpoint": endpoint, "fields": fields}) + "\n")
status, value = 200, {}
if endpoint.endswith("/pulls/7") and method == "GET":
    value = {"state": "open", "draft": False, "mergeable": True,
             "base": {"ref": "main", "sha": base},
             "head": {"ref": "feature/x", "sha": head,
                      "repo": {"full_name": "fixture/repo"}}}
elif "/check-runs?" in endpoint:
    conclusion = "failure" if scenario == "refused" else "success"
    value = {"total_count": 1, "check_runs": [
        {"name": "verify", "id": 1, "app": {"id": 1},
         "status": "completed", "conclusion": conclusion}]}
elif "/actions/runs?" in endpoint:
    value = {"total_count": 0, "workflow_runs": []}
elif endpoint.endswith("/status") and method == "GET":
    value = {"state": "success", "statuses": []}
elif endpoint.endswith("/merge") and method == "PUT":
    if scenario == "unknown":
        status, value = 502, {"message": "Gateway timeout, merge status uncertain"}
    else:
        status, value = 200, {"merged": True, "sha": merge}
elif "/git/ref/heads/feature/x" in endpoint and method == "GET":
    value = {"object": {"sha": head}}
elif "/git/refs/heads/feature/x" in endpoint and method == "DELETE":
    status = 503 if scenario == "post_fail" else 204
    value = {"message": "ref deletion unavailable"} if status == 503 else {}
elif "/actions/workflows/ci.yml/dispatches" in endpoint and method == "POST":
    status, value = 204, {}
elif "/issues/7/comments" in endpoint and method == "POST":
    status, value = 201, {"id": 123}
else:
    raise SystemExit(f"unexpected API call: {method} {endpoint}")
print(f"HTTP/2.0 {status} Fixture")
print("content-type: application/json")
print()
if status != 204:
    print(json.dumps(value))
raise SystemExit(1 if status >= 400 else 0)
'''


def run_scenario(scenario: str):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stub = root / "gh"
        stub.write_text(GITHUB_STUB, encoding="utf-8")
        stub.chmod(0o755)
        log = root / "calls.jsonl"
        environment = {
            **os.environ,
            "PATH": f"{root}{os.pathsep}{os.environ['PATH']}",
            "RELEASED_SCENARIO": scenario,
            "FAKE_GH_CALLS": str(log),
        }
        result = subprocess.run(
            [
                sys.executable, str(TOOL / "scripts" / "merge_command.py"),
                "--command", "/merge",
                "--repository", "fixture/repo",
                "--pull-request-number", "7",
                "--actor", "fixture",
                "--repository-owner", "fixture",
                "--stable-ref", "main",
                "--lane-refs-json", '["dev-cad","dev-ci"]',
                "--permanent-refs-json", '["build","gh-pages"]',
                "--temporary-prefixes-json", '["feature/"]',
                "--integration-workflow", "ci.yml",
            ],
            cwd=ROOT, env=environment, text=True, capture_output=True,
        )
        calls = [json.loads(line) for line in log.read_text().splitlines()]
    return result, calls


def require(test: bool, description: str):
    if not test:
        raise RuntimeError(description)


def main():
    require((TOOL / "scripts" / "merge_command.py").exists(),
            "released merge command is absent")
    for name in ("refused", "unknown", "post_fail", "success"):
        result, calls = run_scenario(name)
        merged = [v for v in calls if v["endpoint"].endswith("/merge")]
        comments = [v for v in calls if v["endpoint"].endswith("/comments")]
        require(len(comments) == 1, f"{name}: expected one outcome comment")
        body = comments[0]["fields"]["body"]
        if name == "refused":
            require(result.returncode != 0 and not merged,
                    "refused: must not call merge")
            require("Merge refused before merge" in body, "refusal not reported")
        elif name == "unknown":
            require(result.returncode != 0 and len(merged) == 1,
                    "unknown: must not claim unattempted merge")
            require("MERGE OUTCOME UNKNOWN" in body,
                    "unknown merge outcome was not distinguished")
        elif name == "post_fail":
            require(result.returncode != 0 and len(merged) == 1,
                    "post_fail: merge and failed lifecycle required")
            require(MERGE in body and "post-merge processing FAILED" in body,
                    "post_fail: accepted SHA/failure not reported")
            require(any("/dispatches" in v["endpoint"] for v in calls),
                    "post_fail: independent stable-base dispatch skipped")
        else:
            require(result.returncode == 0 and len(merged) == 1,
                    f"success: unexpected return code {result.returncode}, {result.stderr}")
            require(MERGE in body and "post-merge" not in body,
                    "success: accepted merge not reported")
        print(f"released merge command: {name} contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

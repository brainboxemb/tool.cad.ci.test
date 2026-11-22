#!/usr/bin/env python3
"""Black-box acceptance for live concise CAD-CI execution logging."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case

SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "logging_case")
    process = subprocess.Popen(
        [sys.executable, "-m", "cad_ci_tool", "run", "--repo", str(repo)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
    )
    assert process.stdout is not None

    lines: list[str] = []
    while True:
        line = process.stdout.readline()
        if line:
            lines.append(line)
            if "logging-consumer-start" in line:
                assert process.poll() is None, "consumer output was buffered until exit"
                break
            continue
        if process.poll() is not None:
            raise AssertionError("early consumer output was not visible before exit")

    remainder, _ = process.communicate(timeout=20)
    output = "".join(lines) + remainder
    assert process.returncode == 0, output
    assert "CAD CI run: logging-case:run" in output, output
    assert "logging-consumer-start" in output, output
    assert "logging-consumer-end" in output, output
    assert "_execute_bundle(" not in output, output
    assert "built: logging-case:run" in output, output

    print("logging_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

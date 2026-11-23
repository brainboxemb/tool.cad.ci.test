#!/usr/bin/env python3
"""Inspect only the public verification-wheel environment contract."""

from __future__ import annotations

import json
import os
from pathlib import Path
import zipfile


def main() -> int:
    wheel_value = os.environ.get("CAD_CI_VERIFICATION_WHEEL", "").strip()
    if not wheel_value:
        raise RuntimeError("CAD_CI_VERIFICATION_WHEEL is required")

    wheel = Path(wheel_value)
    if not wheel.is_file() or wheel.suffix != ".whl":
        raise RuntimeError("verification wheel is missing or invalid")

    with zipfile.ZipFile(wheel) as archive:
        metadata_names = [
            name
            for name in archive.namelist()
            if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise RuntimeError("verification wheel must contain one METADATA")
        metadata = archive.read(metadata_names[0]).decode("utf-8")

    version = next(
        (
            line.removeprefix("Version: ").strip()
            for line in metadata.splitlines()
            if line.startswith("Version: ")
        ),
        "",
    )
    if version != "0.16.0":
        raise RuntimeError(f"unexpected verification package version: {version}")

    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "wheel.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "wheel": wheel.name,
                "version": version,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

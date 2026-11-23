"""Source-architecture contracts for numbered synthetic test roots."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


ROOT_NAME = re.compile(r"^(\d{3})_[a-z0-9][a-z0-9_]*$")
FORBIDDEN_EXECUTION_KEYS = {"steps", "run"}


def _load_mapping(path: Path) -> dict[str, Any]:
    """Load one YAML mapping with a useful source-path error."""

    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected YAML mapping: {path}")
    return value


def _execution_keys(value: Any, prefix: str = "") -> list[str]:
    """Return nested item/repository execution keys that belong in builders."""

    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            name = str(key)
            location = f"{prefix}.{name}" if prefix else name
            if name in FORBIDDEN_EXECUTION_KEYS:
                found.append(location)
            found.extend(_execution_keys(child, location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            location = f"{prefix}[{index}]"
            found.extend(_execution_keys(child, location))
    return found


def validate_test_roots(repo_root: Path) -> dict[str, int]:
    """Enforce the declarative numbered test-root architecture."""

    roots_dir = repo_root / "test_roots"
    if not roots_dir.is_dir():
        raise RuntimeError("missing test_roots directory")

    errors: list[str] = []
    roots: list[tuple[int, Path]] = []

    for child in sorted(path for path in roots_dir.iterdir() if path.is_dir()):
        match = ROOT_NAME.fullmatch(child.name)
        if match is None:
            errors.append(f"unexpected non-numbered test-root directory: {child}")
            continue
        roots.append((int(match.group(1)), child))

    numbers = [number for number, _ in roots]
    expected = list(range(1, len(roots) + 1))
    if numbers != expected:
        errors.append(
            "test-root numbers must be contiguous from 001: "
            f"found {numbers}, expected {expected}"
        )

    builder_count = 0
    item_config_count = 0

    for _, root in roots:
        for required in ("README.md", "cad-ci.yml", "check.py"):
            if not (root / required).is_file():
                errors.append(f"{root.name}: missing required {required}")

        cad_path = root / "cad-ci.yml"
        if not cad_path.is_file():
            continue

        cad = _load_mapping(cad_path)
        execution = _execution_keys(cad)
        if execution:
            errors.append(
                f"{root.name}/cad-ci.yml contains execution keys "
                f"{execution}; execution belongs in builders"
            )

        builders = cad.get("builders")
        if not isinstance(builders, dict) or not builders:
            errors.append(f"{root.name}: cad-ci.yml must declare builders")
            builders = {}

        for name, relative in builders.items():
            builder_count += 1
            if not isinstance(relative, str):
                errors.append(f"{root.name}: builder {name!r} path is not a string")
                continue
            if not relative.startswith("ci/builders/"):
                errors.append(
                    f"{root.name}: builder {name!r} must live below "
                    f"ci/builders/, got {relative!r}"
                )
                continue
            builder_yml = root / relative / "builder.yml"
            if not builder_yml.is_file():
                errors.append(
                    f"{root.name}: builder {name!r} missing {builder_yml.relative_to(root)}"
                )

        templates = cad.get("templates")
        if not isinstance(templates, dict):
            templates = {}

        item_configs = sorted(root.rglob("ci.yml"))
        for item_path in item_configs:
            if "builders" in item_path.parts:
                continue
            item_config_count += 1
            item = _load_mapping(item_path)
            execution = _execution_keys(item)
            if execution:
                errors.append(
                    f"{item_path.relative_to(repo_root)} contains execution keys "
                    f"{execution}; execution belongs in builder.yml"
                )

            builder = item.get("builder")
            template = item.get("template")
            if builder is None and isinstance(template, str):
                template_data = templates.get(template)
                if not isinstance(template_data, dict):
                    errors.append(
                        f"{item_path.relative_to(repo_root)} references unknown "
                        f"template {template!r}"
                    )
                else:
                    builder = template_data.get("builder")

            if not isinstance(builder, str):
                errors.append(
                    f"{item_path.relative_to(repo_root)} must select a builder "
                    "directly or through its template"
                )
            elif builder not in builders:
                errors.append(
                    f"{item_path.relative_to(repo_root)} selects undeclared "
                    f"builder {builder!r}"
                )

        for legacy in sorted(root.rglob("run.py")):
            if "builders" not in legacy.parts:
                errors.append(
                    f"{legacy.relative_to(repo_root)} is legacy item execution; "
                    "move execution into ci/builders/"
                )

    if errors:
        raise RuntimeError(
            "declarative test-root contract failed:\n- " + "\n- ".join(errors)
        )

    summary = {
        "roots": len(roots),
        "builders": builder_count,
        "item_configs": item_config_count,
    }
    print(
        "test-root architecture accepted: "
        f"{summary['roots']} roots, "
        f"{summary['builders']} builders, "
        f"{summary['item_configs']} item configs",
        flush=True,
    )
    return summary

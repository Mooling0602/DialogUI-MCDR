#!/usr/bin/env python3
"""Edit pyproject.toml and gitrepo.toml with project metadata."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import cast


def _dump_toml_section(data: dict[str, object], prefix: str = "") -> list[str]:
    """Recursively serialize a TOML section."""
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            full_key = f"{prefix}.{key}" if prefix else key
            val_dict = cast("dict[str, object]", value)
            if _all_values_are_dicts(val_dict):
                lines.extend(_dump_toml_section(val_dict, full_key))
            elif _has_nested_dict(val_dict):
                lines.append("")
                lines.append(f"[{full_key}]")
                lines.extend(_dump_toml_section(val_dict, full_key))
            else:
                lines.append("")
                lines.append(f"[{full_key}]")
                for sub_key, sub_value in val_dict.items():
                    lines.append(f"{sub_key} = {_format_value(sub_value)}")
        else:
            lines.append(f"{key} = {_format_value(value)}")
    return lines


def _all_values_are_dicts(d: dict[str, object]) -> bool:
    return len(d) > 0 and all(isinstance(v, dict) for v in d.values())


def _has_nested_dict(d: dict[str, object]) -> bool:
    return any(isinstance(v, dict) for v in d.values())


def _dump_toml(data: dict[str, object]) -> list[str]:
    """Serialize top-level TOML document."""
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            val_dict = cast("dict[str, object]", value)
            if _all_values_are_dicts(val_dict):
                lines.extend(_dump_toml_section(val_dict, key))
            elif _has_nested_dict(val_dict):
                lines.append("")
                lines.append(f"[{key}]")
                lines.extend(_dump_toml_section(val_dict, key))
            else:
                lines.append("")
                lines.append(f"[{key}]")
                for sub_key, sub_value in val_dict.items():
                    lines.append(f"{sub_key} = {_format_value(sub_value)}")
        else:
            lines.append(f"{key} = {_format_value(value)}")
    lines.append("")
    return lines


def _format_value(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, list):
        items = ", ".join(_format_value(v) for v in value)
        return f"[{items}]"
    if isinstance(value, dict):
        items = ", ".join(
            f"{_format_key(cast(str, k))} = {_format_value(v)}"
            for k, v in value.items()
        )
        return f"{{ {items} }}"
    return str(value)


def _format_key(key: str) -> str:
    if key.isidentifier() and not _is_bare_key_reserved(key):
        return key
    escaped = key.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _is_bare_key_reserved(key: str) -> bool:
    return key.lower() in {"true", "false", "inf", "nan", "none"}


def _write_toml(path: Path, data: dict[str, object]) -> None:
    lines = _dump_toml(data)
    path.write_text("\n".join(lines), encoding="utf-8")


def _sorted_table_order(data: dict[str, object], order: list[str]) -> dict[str, object]:
    """Re-order keys to match the original file layout."""
    result: dict[str, object] = {}
    for key in order:
        if key in data:
            result[key] = data[key]
    for key, value in data.items():
        if key not in result:
            result[key] = value
    return result


def project_setup(
    repo_name: str,
    *,
    package_name: str | None = None,
    description: str = "",
    author_name: str,
    author_email: str | None = None,
    working_dir: str = ".",
) -> None:
    root = Path(working_dir).resolve()
    if not root.is_dir():
        print(f"Error: '{working_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    pyproject_path = root / "pyproject.toml"
    gitrepo_path = root / "gitrepo.toml"

    if not pyproject_path.is_file():
        print(f"Error: '{pyproject_path}' not found.", file=sys.stderr)
        sys.exit(1)
    if not gitrepo_path.is_file():
        print(f"Error: '{gitrepo_path}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        pyproject_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as e:
        print(f"Error: Failed to parse '{pyproject_path}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        gitrepo_data = tomllib.loads(gitrepo_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as e:
        print(f"Error: Failed to parse '{gitrepo_path}': {e}", file=sys.stderr)
        sys.exit(1)

    pyproject_data["project"]["name"] = package_name if package_name else repo_name
    pyproject_data["project"]["description"] = description
    if author_email:
        pyproject_data["project"]["authors"] = [
            {"name": author_name, "email": author_email}
        ]
    else:
        pyproject_data["project"]["authors"] = [{"name": author_name}]

    gitrepo_data["meta"]["name"] = repo_name
    gitrepo_data["meta"]["description"] = description
    gitrepo_data["meta"]["author"] = [{"github": author_name}]

    pyproject_data = _sorted_table_order(
        pyproject_data, ["build-system", "project", "dependency-groups", "tool"]
    )
    gitrepo_data = _sorted_table_order(gitrepo_data, ["meta", "platform"])

    try:
        _write_toml(pyproject_path, pyproject_data)
        _write_toml(gitrepo_path, gitrepo_data)
    except OSError as e:
        print(f"Error: Failed to write file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Updated: {pyproject_path}")
    print(f"Updated: {gitrepo_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Edit pyproject.toml and gitrepo.toml with project metadata.",
    )
    parser.add_argument(
        "repo_name",
        help="Repository name (used for gitrepo.toml meta name)",
    )
    parser.add_argument(
        "--package-name",
        default=None,
        help="UV package name for pyproject.toml (default: same as repo_name)",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Project description (default: empty)",
    )
    parser.add_argument(
        "--author-name",
        required=True,
        help="Author name (GitHub username)",
    )
    parser.add_argument(
        "--author-email",
        default=None,
        help="Author email (optional, omitted if not provided)",
    )
    parser.add_argument(
        "working_dir",
        nargs="?",
        default=".",
        help="Working directory containing pyproject.toml and gitrepo.toml (default: .)",
    )
    args = parser.parse_args()
    project_setup(
        args.repo_name,
        package_name=args.package_name,
        description=args.description,
        author_name=args.author_name,
        author_email=args.author_email,
        working_dir=args.working_dir,
    )


if __name__ == "__main__":
    main()

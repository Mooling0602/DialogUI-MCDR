#!/usr/bin/env python3
import argparse
import fnmatch
import json
import sys
from pathlib import Path


def _parse_gitignore(path: Path) -> list[tuple[bool, str]]:
    """Parse a gitignore-like file.

    Returns a list of (negate, pattern) tuples.  negate=True means the
    pattern is a negation (``!pattern``).  Trailing slashes are stripped
    (we are only matching directory names).
    """
    if not path.is_file():
        return []

    patterns: list[tuple[bool, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#"):
            continue
        negate = False
        if line.startswith("!"):
            negate = True
            line = line[1:]
        line = line.rstrip("/")
        line = line.lstrip("/")
        if line:
            patterns.append((negate, line))
    return patterns


def _is_ignored(name: str, patterns: list[tuple[bool, str]]) -> bool:
    """Return True when *name* should be excluded according to gitignore rules."""
    ignored = False
    for negate, pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            ignored = not negate
    return ignored


def modify_plugin_package(
    src_dir: str = ".",
    *,
    ignore_patterns: list[str] | None = None,
    ignore_file: str = ".gitignore",
    pyproject_dir: str | None = None,
) -> None:
    src = Path(src_dir).resolve()
    if not src.is_dir():
        print(f"Error: '{src_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    json_path = src / "mcdreforged.plugin.json"
    if not json_path.is_file():
        print(f"Error: '{json_path}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        meta = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse '{json_path}': {e}", file=sys.stderr)
        sys.exit(1)

    plugin_id: str | None = meta.get("id")
    if not plugin_id:
        print(
            f"Error: 'id' field not found or empty in '{json_path}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    if ignore_patterns is not None:
        patterns = [(False, p.rstrip("/").lstrip("/")) for p in ignore_patterns if p]
    else:
        ignore_path = src / ignore_file
        patterns = _parse_gitignore(ignore_path)

    patterns.insert(0, (False, "tools"))

    dirs = [
        d for d in src.iterdir() if d.is_dir() and not _is_ignored(d.name, patterns)
    ]

    if len(dirs) == 0:
        print(f"No plugin package directory found in '{src}'.")
        return

    if len(dirs) > 1:
        names = [d.name for d in dirs]
        print(
            f"Error: Multiple plugin package directories found: {names}. "
            f"Only one is allowed, delete the extra ones or add it to ignore lists.",
            file=sys.stderr,
        )
        sys.exit(1)

    target = dirs[0]
    if target.name == plugin_id:
        print(
            f"Plugin package directory is already named '{plugin_id}', nothing to do."
        )
        return

    new_path = src / plugin_id
    if new_path.exists():
        print(
            f"Error: Cannot rename '{target.name}' to '{plugin_id}' "
            f"because '{new_path}' already exists.",
            file=sys.stderr,
        )
        sys.exit(1)

    target.rename(new_path)
    print(f"Renamed: {target} -> {new_path}")

    if pyproject_dir is not None:
        pp_dir = Path(pyproject_dir)
    else:
        pp_dir = src.parent

    pp = pp_dir / "pyproject.toml"
    if not pp.is_file():
        print(
            f"Error: 'pyproject.toml' not found at '{pp}'. "
            f"Provide the directory with --pyproject-dir.",
            file=sys.stderr,
        )
        sys.exit(1)

    content = pp.read_text(encoding="utf-8")
    old_entry = f'"src/{target.name}"'
    new_entry = f'"src/{plugin_id}"'
    if old_entry not in content:
        print(
            f"Warning: Could not find '{old_entry}' in '{pp}', "
            f"skipping pyproject.toml update.",
        )
        return

    content = content.replace(old_entry, new_entry)
    pp.write_text(content, encoding="utf-8")
    print(f"Updated: {pp}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename the plugin package directory to match the plugin id.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=".",
        help="The input directory which the plugin is in (default: .)",
    )
    parser.add_argument(
        "--ignore-patterns",
        nargs="*",
        default=None,
        help="Gitignore-like patterns to ignore during directory scanning.",
    )
    parser.add_argument(
        "--ignore-file",
        default=".gitignore",
        help="Path to a gitignore-like file (default: .gitignore)",
    )
    parser.add_argument(
        "--pyproject-dir",
        default=None,
        help="Directory containing pyproject.toml (default: <INPUT>/..)",
    )
    args = parser.parse_args()
    modify_plugin_package(
        args.input,
        ignore_patterns=args.ignore_patterns,
        ignore_file=args.ignore_file,
        pyproject_dir=args.pyproject_dir,
    )


if __name__ == "__main__":
    main()

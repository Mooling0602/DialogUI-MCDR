#!/usr/bin/env python3
"""Interactive setup tool for creating a new MCDR plugin from the template."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from src.tools.i18n import t
from src.tools.modify_plugin_package import modify_plugin_package
from src.tools.plugin_meta import get_input
from src.tools.plugin_meta import main as run_plugin_meta
from src.tools.project_setup import project_setup

ROOT = Path(__file__).resolve().parent


def confirm(prompt: str, default: bool = True) -> bool:
    suffix = " (Y/n): " if default else " (y/N): "
    full_prompt = f"{prompt}{suffix}"
    answer = input(full_prompt).strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def _get_git_author_name() -> str | None:
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            name = result.stdout.strip()
            if name:
                return name
    except OSError:
        pass
    return None


def run_setup() -> None:
    print("--- MCDR Plugin Setup ---")
    print()

    repo_name = ""
    while not repo_name.strip():
        repo_name = get_input(t("Enter repository name:"), "").strip()
        if not repo_name:
            print("Repository name is required.")

    package_name = get_input(t("Enter UV package name:"), repo_name).strip()
    if not package_name:
        package_name = repo_name

    description = get_input(t("Enter description (optional):"), "").strip()

    author_name: str
    if confirm(t("Do you want to get the author information from git?")):
        git_name = _get_git_author_name()
        if git_name:
            author_name = git_name
            print(f"Found: {author_name}")
        else:
            print(t("Failed to get author info from git."))
            author_name = _ask_author_name()
    else:
        author_name = _ask_author_name()

    author_email_input = get_input(t("Enter author email (optional):"), "")
    author_email = author_email_input.strip() if author_email_input.strip() else None

    print()
    project_setup(
        repo_name,
        package_name=package_name,
        description=description,
        author_name=author_name,
        author_email=author_email,
    )

    print()
    if confirm(t("Create the plugin now?")):
        dst = ROOT / "src"
        run_plugin_meta(working_dir=dst)
        modify_plugin_package(str(dst))
    else:
        print(
            t(
                "Tip: You can run 'python3 -m tools.plugin_meta' and "
                "'python3 -m tools.modify_plugin_package src' later to "
                "create the plugin."
            )
        )


def _ask_author_name() -> str:
    name = ""
    while not name.strip():
        name = get_input(t("Enter author name:"), "").strip()
        if not name:
            print("Author name is required.")
    return name


def run_remove() -> None:
    if not confirm(
        t("This will remove the management tool. It cannot be undone. Continue?")
    ):
        print(t("Removal cancelled."))
        return

    keep_clean = confirm(t("Keep '{filename}' tool?", filename="clean_pycache.py"))
    keep_setup = confirm(t("Keep '{filename}' tool?", filename="setup.py"))
    keep_doc = confirm(t("Keep documentations in 'doc/' directory?"))

    scripts_to_remove = ["check.py"]
    if not keep_clean:
        scripts_to_remove.append("clean_pycache.py")
    if not keep_setup:
        scripts_to_remove.append("setup.py")

    for script in scripts_to_remove:
        path = ROOT / script
        if path.is_file():
            path.unlink()
            print(t("Removed: {path}", path=str(path)))

    if not keep_doc:
        doc_dir = ROOT / "doc"
        if doc_dir.is_dir():
            shutil.rmtree(doc_dir)
            print(t("Removed: {path}", path=str(doc_dir)))

    tools_dir = ROOT / "src" / "tools"
    if tools_dir.is_dir():
        shutil.rmtree(tools_dir)
        print(t("Removed: {path}", path=str(tools_dir)))

    if __file__ is not None:
        self_path = Path(__file__).resolve()
        if self_path.is_file():
            self_path.unlink(missing_ok=True)

    print()
    print(t("Removal complete."))


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        run_remove()
    else:
        run_setup()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import copy
import json
import sys
from pathlib import Path
from typing import NotRequired, TypedDict

from .i18n import t

# Try to import prompt_toolkit, if import fails, use builtin input
try:
    from prompt_toolkit import prompt

    use_prompt_toolkit = True
except ImportError:
    use_prompt_toolkit = False


class PluginMeta(TypedDict):
    id: str
    version: str
    name: str
    description: dict[str, str]
    author: str
    link: str
    dependencies: dict[str, str]
    entrypoint: NotRequired[str | None]
    resources: NotRequired[list[str]]


# Template content for plugin metadata
meta_template: PluginMeta = {
    "id": "plugin_id",
    "version": "0.0.1",
    "name": "Plugin",
    "description": {"en_us": "Description of this plugin.", "zh_cn": "此插件的介绍。"},
    "author": "Unknown",
    "link": "https://github.com",
    "dependencies": {"mcdreforged": ">=2.14.1"},
    "entrypoint": None,  # Optional
    "resources": ["lang"],  # Optional
}


def get_input(prompt_text: str, default: object) -> str:
    """
    Prompt the user for input, and return the default value if the input is empty.
    When using prompt_toolkit, a better editing experience can be enjoyed.
    """
    default_str = str(default) if default is not None else ""
    full_prompt = f"{prompt_text}{t(' (Default: {default}): ', default=default_str)}"
    if use_prompt_toolkit:
        user_input = prompt(full_prompt, default=default_str)
    else:
        user_input = input(full_prompt)
    if user_input.strip() == "":
        return str(default) if default is not None else ""
    return user_input


def main(working_dir: Path | None = None):
    if working_dir is None:
        working_dir = Path.cwd()
    working_dir = working_dir.resolve()
    # Deep copy the template to avoid modifying the original template
    meta: PluginMeta = copy.deepcopy(meta_template)

    # Prompt user for plugin metadata
    meta["id"] = get_input(t("Enter plugin id:"), meta["id"])
    meta["version"] = get_input(t("Enter plugin version:"), meta["version"])
    meta["name"] = get_input(t("Enter plugin name:"), meta["name"])
    meta["description"]["en_us"] = get_input(
        t("Enter English description:"), meta["description"]["en_us"]
    )
    meta["description"]["zh_cn"] = get_input(
        t("Enter Chinese(Simplified) description:"), meta["description"]["zh_cn"]
    )
    meta["author"] = get_input(t("Enter author:"), meta["author"])
    meta["link"] = get_input(t("Enter repo link:"), meta["link"])
    meta["dependencies"]["mcdreforged"] = get_input(
        t("Enter mcdreforged dependency version:"), meta["dependencies"]["mcdreforged"]
    )

    entrypoint_input = get_input(t("Enter entrypoint (optional):"), meta["entrypoint"])
    if entrypoint_input != "" and entrypoint_input is not None:
        meta["entrypoint"] = entrypoint_input
    else:
        del meta["entrypoint"]

    # Process resources list, default to template's processing
    resources_default = ", ".join(meta["resources"]) if meta["resources"] else ""
    resources_input = get_input(
        t("Enter resource list (comma-separated, optional):"), resources_default
    )
    if resources_input.strip() == "":
        meta["resources"] = meta_template["resources"]
    else:
        meta["resources"] = [
            item.strip() for item in resources_input.split(",") if item.strip()
        ]

    # Output filename
    output_filename = "mcdreforged.plugin.json"

    # Write JSON to file (ensure Chinese characters will be not escaped)
    with open(working_dir / output_filename, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)

    print(t("Successfully generated JSON file: {filename}", filename=output_filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(Path(sys.argv[1]))
    else:
        main()

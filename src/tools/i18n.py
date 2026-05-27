import locale
import os

_translations_zh_cn: dict[str, str] = {
    " (Default: {default}): ": "（默认：{default}）：",
    "Enter plugin id:": "输入插件 ID：",
    "Enter plugin version:": "输入插件版本：",
    "Enter plugin name:": "输入插件名称：",
    "Enter English description:": "输入英文介绍：",
    "Enter Chinese(Simplified) description:": "输入简体中文介绍：",
    "Enter author:": "输入作者：",
    "Enter repo link:": "输入仓库链接：",
    "Enter mcdreforged dependency version:": "输入 MCDReforged 依赖版本：",
    "Enter entrypoint (optional):": "输入入口点（可选）：",
    "Enter resource list (comma-separated, optional):": "输入资源列表（逗号分隔，可选）：",
    "Successfully generated JSON file: {filename}": "成功生成 JSON 文件：{filename}",
    "Enter repository name:": "输入仓库名称：",
    "Enter UV package name:": "输入 UV 包名：",
    "Enter description (optional):": "输入描述（可选）：",
    "Do you want to get the author information from git? (Y/n): ": "是否从 Git 获取作者信息？（Y/n）：",
    "Enter author name (GitHub username):": "输入作者名称（GitHub 用户名）：",
    "Enter author email (optional):": "输入作者邮箱（可选）：",
    "Create the plugin now? (Y/n): ": "是否现在创建插件？（Y/n）：",
    "Tip: You can run 'python3 -m tools.plugin_meta' and 'python3 -m tools.modify_plugin_package src' later to create the plugin.": "提示：之后可运行 'python3 -m tools.plugin_meta' 和 'python3 -m tools.modify_plugin_package src' 来创建插件。",
    "This will remove the management tool. It cannot be undone. Continue? (Y/n): ": "这将移除管理工具，不可撤销。是否继续？（Y/n）：",
    "Keep '{filename}' tool? (Y/n): ": "保留 '{filename}' 工具吗？（Y/n）：",
    "Keep documentations in 'doc/' directory? (Y/n): ": "保留 'doc/' 目录下的文档吗？（Y/n）：",
    "Removed: {path}": "已移除：{path}",
    "Removal complete.": "移除完成。",
    "Removal cancelled.": "已取消移除。",
    "Error: 'uv' not found. Please install UV first: https://docs.astral.sh/uv/": "错误：未找到 'uv'。请先安装 UV：https://docs.astral.sh/uv/",
    "Failed to get author info from git.": "从 Git 获取作者信息失败。",
    "Running 'uv sync'...": "正在运行 'uv sync'...",
    "'uv sync' completed.": "'uv sync' 完成。",
    "'uv sync' failed with exit code {code}.": "'uv sync' 失败，退出码 {code}。",
    "Enter author name:": "输入作者名称：",
    "Failed to get author info from git: {error}": "从 Git 获取作者信息失败：{error}",
    "Setup cancelled.": "已取消安装。",
    "Plugin creation cancelled.": "已取消插件创建。",
}


def _detect_language() -> str:
    lang = os.environ.get("LANG", "") or locale.getdefaultlocale()[0] or ""
    if lang.startswith("zh"):
        return "zh_cn"
    return "en_us"


_current_lang = _detect_language()


def t(fallback: str, **kwargs: object) -> str:
    text = fallback
    if _current_lang == "zh_cn":
        translated = _translations_zh_cn.get(fallback)
        if translated is not None:
            text = translated
    if kwargs:
        return text.format(**kwargs)
    return text


def set_language(lang: str) -> None:
    global _current_lang
    _current_lang = lang

# Source Code Management

We use [UV](https://docs.astral.sh/uv) to manage the source code of this plugin.

The management tool is located in the `src/tools` directory, use `python3 main.py` in the root directory of this repository to run it.

## Management Tool

If you start the tool by running `main.py`, it will ask you several questions to help you create a new plugin project.

Here are the questions it will ask you:

> Call `src/tools/project_setup.py` at the beginning to setup the project.

1. **Repository Name** (necessary): The name of the repository you want to create, used for git control.

2. **UV Package Name** (necessary): The name of the python package you want to create, used for UV control.

3. **Description** (optional): A brief description of the plugin project.

4. Do you want to get the author information from git? (Y/n)

> - If yes, tool will try to get the author information from git.
>
> - If no, you have to manually input the author information.

5. **Author Name** (necessary if yes in step 4): Your GitHub username.

6. **Author Email** (optional): Your GitHub email.

> Email is not required for creating the plugin metadata or committing plugin to [PluginCatalogue](https://github.com/MCDReforged/PluginCatalogue), so it's optional.

1. Create the plugin now? (Y/n)

> If yes, the `main.py` will call first `src/tools/plugin_meta.py` to generate the plugin metadata(mcdreforged.plugin.json), then call `src/tools/modify_plugin_package.py` to sync changes to plugin package and `pyproject.toml`; else tip you to do it manually.

## GitHub Workflows

We use GitHub workflows to manage the release process of this plugin. Configurations and related scripts are in the `.github` directory.

## Remove the Management Tool

After everything is setup, you may want to remove the management tool from the repository.

Just run `python3 main.py --remove`, the management tool will guide you to remove it:

- Confirm the removal? It cannot be undone. (Y/n)

> If no, the tool will exit and do nothing.

1. Removing Management Tools...
2. Keep `clean_pycache.py` tool? (Y/n)
3. Keep `setup.py` tool? (Y/n)
4. Keep documentations in `doc/`? (Y/n)
5. Removing `main.py`...


# Plugin Structure
```sh
$ tree .
.
├── doc
│   ├── PluginStructure.md         # This documentation.
│   └── RELEASE.md                 # Release specification.
├── src                            # Source code directory.
│   ├── tools                      # Tools for creating a new MCDR plugin.
│   │   ├── __init__.py            # Tools entrypoint module.
│   │   ├── plugin_meta.py         # Plugin metadata(mcdreforged.plugin.json) generator.
│   │   └── ...                    # Other tools modules.
│   ├── plugin_id                  # Plugin source code directory.
│   │   ├── __init__.py            # Plugin entrypoint module.
│   │   └── ...                    # Other plugin modules.
│   └── mcdreforged.plugin.json    # Plugin configuration file.
├── .gitignore                     # Git ignore file.
├── check.py                       # Check the code with Ruff and Ty.
├── clean_pycache.py               # Clean the Python cache folders.
├── gitrepo.toml                   # Git repository configuration, will be used for CI.
├── LICENSE                        # License of this project.
├── main.py                        # Main entry point of the tools to create a new MCDR plugin.
├── pyproject.toml                 # UV configuration file of this project.
├── README_*.md                    # I18n README files.
├── README.md                      # Main README file.
├── setup.py                       # Init UV virtual environment to install dependencies.
└── ...
```
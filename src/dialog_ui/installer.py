import pathlib
import shutil

from mcdreforged.api.all import PluginServerInterface

from dialog_ui.utils import extract_file


def get_datapack_dir(server: PluginServerInterface) -> pathlib.Path:
    """Get the path to the datapack directory for this plugin.

    :param server: PluginServerInterface
    """
    server_dir = pathlib.Path(
        server.get_mcdr_config().get("working_directory", "server")
    )
    return server_dir / "world" / "datapacks"


def install_datapack(server: PluginServerInterface, force: bool = False):
    """Install the new built datapack.

    :param server: PluginServerInterface
    :param force: whether reinstall new and override present datapack to backups, defaults to False
    """
    datapack_id = "mcdr_dialog"
    resource_root = f"resources/datapacks/{datapack_id}"
    resource_files = [
        "pack.mcmeta",
        "data/mcdr_dialog/dialog/main_screen.json",
        "data/mcdr_dialog/dialog/test_text_input.json",
        "data/minecraft/tags/dialog/pause_screen_additions.json",
    ]

    datapack_dir = get_datapack_dir(server)
    target_root = datapack_dir / datapack_id
    backup_root = datapack_dir / f"{datapack_id}.old"

    if target_root.exists():
        if not force:
            server.logger.info("Datapack already exists at %s", target_root)
            return
        if backup_root.exists():
            shutil.rmtree(backup_root)
        shutil.move(str(target_root), str(backup_root))

    target_root.mkdir(parents=True, exist_ok=True)

    for rel_path in resource_files:
        target_path = target_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        extract_file(server, f"{resource_root}/{rel_path}", str(target_path))

    server.logger.info("Installed datapack at %s", target_root)


def install_resource_pack(server: PluginServerInterface):
    """Install the new built resource pack.

    :param server: PluginServerInterface
    """
    server.logger.warning(
        "Need a remote file server to install resource pack, and this feature is not implemented yet."
    )

from mcdreforged.api.all import (
    CommandContext,
    CommandSource,
    PluginServerInterface,
    SimpleCommandBuilder,
)

from dialog_ui.installer import install_datapack

builder = SimpleCommandBuilder()
_command_confirmation: bool = False


def on_load(server: PluginServerInterface, _):
    builder.register(server)
    server.logger.info("DialogUI loaded.")


@builder.command("!!dialog")
def open_dialog(src: CommandSource):
    if not src.is_player:
        src.reply("This command can only be used in-game.")
        return
    server = src.get_server().psi()
    server.execute(f"dialog show {src.player} mcdr_dialog:main_screen")  # ty:ignore[unresolved-attribute]


@builder.command("!!dialog reinstall")
def reinstall_dialog(src: CommandSource, ctx: CommandContext):
    global _command_confirmation
    if not src.has_permission(4):
        src.reply("You don't have permission to use this command.")
        return
    if not _command_confirmation and "--confirm" not in ctx.command:
        src.reply("Retype this command to confirm the dangerous option.")
        return
    server = src.get_server().psi()
    install_datapack(server, force=True)
    _command_confirmation = False


def on_unload(server: PluginServerInterface):
    server.logger.info("DialogUI unloaded.")

from mcdreforged.api.all import (
    CommandContext,
    CommandSource,
    PluginServerInterface,
    RText,
    SimpleCommandBuilder,
)
from mcdreforged.minecraft.rtext.click_event import RClickShowDialog

from dialog_ui.installer import install_datapack
from dialog_ui.mcdr_menu.test_text_input import dialog

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


@builder.command("!!dialog menu")
def open_menu(src: CommandSource):
    src.reply(
        "Open " + RText("Menu").set_click_event(RClickShowDialog(dialog.to_dict()))
    )


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

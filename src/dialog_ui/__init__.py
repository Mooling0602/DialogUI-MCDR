from mcdreforged.api.all import PluginServerInterface


def on_load(server: PluginServerInterface, _):
    server.logger.info("DialogUI loaded.")


def on_unload(server: PluginServerInterface):
    server.logger.info("DialogUI unloaded.")

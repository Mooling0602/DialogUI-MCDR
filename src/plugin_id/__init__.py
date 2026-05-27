from mcdreforged.api.all import PluginServerInterface


def on_load(server: PluginServerInterface, _):
    server.logger.info("Plugin loaded.")


def on_unload(server: PluginServerInterface):
    server.logger.info("Plugin unloaded.")

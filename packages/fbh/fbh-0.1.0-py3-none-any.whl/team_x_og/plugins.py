import logging
from typing import Callable
from .handlers import Handler
from .errors import TeamXError

logger = logging.getLogger("TeamXBot.Plugins")

class Plugin:
    def __init__(self, name: str):
        self.name = name
        self.handlers = []
        logger.debug(f"Created plugin: {name}")

    def register_handler(self, handler: Handler):
        self.handlers.append(handler)
        logger.debug(f"Plugin {self.name} registered handler: {handler.type}")

def load_plugin(bot, plugin_path: str):
    try:
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("plugin", plugin_path)
        if not spec:
            raise TeamXError(f"Invalid plugin path: {plugin_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules["plugin"] = module
        spec.loader.exec_module(module)
        plugin = getattr(module, "plugin", None)
        if plugin:
            for handler in plugin.handlers:
                bot.register_handler(handler)
            logger.info(f"Loaded plugin: {plugin.name}")
        else:
            raise TeamXError(f"No plugin defined in {plugin_path}")
    except Exception as e:
        logger.error(f"Error loading plugin {plugin_path}: {e}")
        raise TeamXError(f"Failed to load plugin: {e}")
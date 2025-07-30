from typing import Callable, Dict
from functools import wraps
import logging
from .errors import HandlerError

logger = logging.getLogger("TeamXBot.Handlers")

class Handler:
    def __init__(self, type_: str, pattern: str, callback: Callable):
        self.type = type_
        self.pattern = pattern
        self.callback = callback
        self.bot = None

    def matches(self, update: Dict) -> bool:
        try:
            if self.type == "command":
                message = update.get("message", {}).get("text", "")
                return message.startswith(f"/{self.pattern}")
            return False
        except Exception as e:
            logger.error(f"Error in handler matching: {e}")
            return False

    async def execute(self, update: Dict):
        try:
            if not self.bot:
                raise HandlerError("Bot instance not set for handler")
            await self.callback(self.bot, update)
        except Exception as e:
            logger.error(f"Error executing handler {self.pattern}: {e}")
            raise HandlerError(f"Handler execution failed: {e}")

def command(name: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(bot, update):
            try:
                await func(bot, update)
            except Exception as e:
                logger.error(f"Error in command '{name}': {e}")
                raise HandlerError(f"Command {name} failed: {e}")
        wrapper.handler = Handler("command", name, wrapper)
        logger.debug(f"Registered command: {name}")
        return wrapper
    return decorator
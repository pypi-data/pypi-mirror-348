import aiohttp
import asyncio
import logging
from typing import List, Dict
from .handlers import Handler
from .errors import TokenInvalidError, BotRunningError, APIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TeamXBot")

class TeamXBot:
    _instance = None

    def __init__(self, token: str, parse_mode: str = "Markdown"):
        if not token:
            raise TokenInvalidError("Bot token cannot be empty")
        if TeamXBot._instance is not None:
            raise BotRunningError("A bot instance is already running")
        TeamXBot._instance = self
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.handlers: List[Handler] = []
        self.parse_mode = parse_mode
        self.session = None
        self.is_running = False
        logger.info("TeamXBot initialized")

    def register_handler(self, handler: Handler):
        try:
            handler.bot = self
            self.handlers.append(handler)
            logger.debug(f"Handler registered: {handler.type} - {handler.pattern}")
        except Exception as e:
            logger.error(f"Error registering handler: {e}")
            raise HandlerError(f"Failed to register handler: {e}")

    async def _request(self, method: str, data: Dict = None) -> Dict:
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            url = self.base_url + method
            async with self.session.post(url, json=data) as response:
                result = await response.json()
                if not result.get("ok"):
                    raise APIError(f"API error in {method}: {result.get('description')}")
                return result
        except Exception as e:
            logger.error(f"Request error in {method}: {e}")
            raise APIError(f"Failed to execute {method}: {e}")

    async def send_message(self, chat_id: int, text: str, reply_markup: Dict = None):
        try:
            data = {"chat_id": chat_id, "text": text, "parse_mode": self.parse_mode}
            if reply_markup:
                data["reply_markup"] = reply_markup
            return await self._request("sendMessage", data)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise APIError(f"Failed to send message: {e}")

    async def get_updates(self, offset: int = None) -> List[Dict]:
        try:
            data = {"timeout": 30, "offset": offset}
            result = await self._request("getUpdates", data)
            return result.get("result", [])
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []

    async def start_polling(self):
        if self.is_running:
            raise BotRunningError("Bot is already polling")
        self.is_running = True
        offset = None
        logger.info("Started polling...")
        try:
            while self.is_running:
                updates = await self.get_updates(offset)
                for update in updates:
                    offset = update["update_id"] + 1
                    await self._process_update(update)
                await asyncio.sleep(0.1)  # Avoid CPU overload
        except Exception as e:
            logger.error(f"Polling error: {e}")
            raise
        finally:
            self.is_running = False

    async def _process_update(self, update: Dict):
        try:
            for handler in self.handlers:
                if handler.matches(update):
                    await handler.execute(update)
        except Exception as e:
            logger.error(f"Error processing update: {e}")

    def run(self):
        try:
            import inspect
            caller_frame = inspect.currentframe().f_back
            for name, obj in caller_frame.f_globals.items():
                if hasattr(obj, 'handler'):
                    self.register_handler(obj.handler)
            asyncio.run(self.start_polling())
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
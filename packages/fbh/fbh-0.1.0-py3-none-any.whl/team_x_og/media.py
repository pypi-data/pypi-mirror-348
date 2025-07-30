from typing import Dict
import aiohttp
import logging
from .errors import APIError, TeamXError

logger = logging.getLogger("TeamXBot.Media")

class Media:
    def __init__(self, bot):
        self.bot = bot

    async def send_photo(self, chat_id: int, photo: str, caption: str = None):
        try:
            data = {"chat_id": chat_id, "photo": photo}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = self.bot.parse_mode
            result = await self.bot._request("sendPhoto", data)
            logger.info(f"Sent photo to chat {chat_id}")
            return result
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            raise APIError(f"Failed to send photo: {e}")

    async def send_video(self, chat_id: int, video: str, caption: str = None):
        try:
            data = {"chat_id": chat_id, "video": video}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = self.bot.parse_mode
            result = await self.bot._request("sendVideo", data)
            logger.info(f"Sent video to chat {chat_id}")
            return result
        except Exception as e:
            logger.error(f"Error sending video: {e}")
            raise APIError(f"Failed to send video: {e}")

    async def send_audio(self, chat_id: int, audio: str, caption: str = None):
        try:
            data = {"chat_id": chat_id, "audio": audio}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = self.bot.parse_mode
            result = await self.bot._request("sendAudio", data)
            logger.info(f"Sent audio to chat {chat_id}")
            return result
        except Exception as e:
            logger.error(f"Error sending audio: {e}")
            raise APIError(f"Failed to send audio: {e}")

    async def send_document(self, chat_id: int, document: str, caption: str = None):
        try:
            data = {"chat_id": chat_id, "document": document}
            if caption:
                data["caption"] = caption
                data["parse_mode"] = self.bot.parse_mode
            result = await self.bot._request("sendDocument", data)
            logger.info(f"Sent document to chat {chat_id}")
            return result
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            raise APIError(f"Failed to send document: {e}")

    async def send_file(self, chat_id: int, file_path: str, media_type: str, caption: str = None):
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("chat_id", str(chat_id))
                    data.add_field(media_type, f, filename=file_path)
                    if caption:
                        data.add_field("caption", caption)
                        data.add_field("parse_mode", self.bot.parse_mode)
                    async with session.post(f"{self.bot.base_url}send{media_type.capitalize()}", data=data) as response:
                        result = await response.json()
                        if not result.get("ok"):
                            raise APIError(f"Failed to send {media_type}: {result.get('description')}")
                        logger.info(f"Sent {media_type} file to chat {chat_id}")
                        return result
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise TeamXError(f"File {file_path} not found")
        except Exception as e:
            logger.error(f"Error sending file {file_path}: {e}")
            raise APIError(f"Failed to send file: {e}")
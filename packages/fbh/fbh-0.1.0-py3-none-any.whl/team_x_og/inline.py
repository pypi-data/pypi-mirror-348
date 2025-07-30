from typing import List, Dict
import logging
from .errors import TeamXError

logger = logging.getLogger("TeamXBot.Inline")

class InlineButton:
    def __init__(self, text: str, callback_data: str = None, url: str = None):
        if not text:
            raise TeamXError("Button text cannot be empty")
        if callback_data and url:
            raise TeamXError("Button cannot have both callback_data and url")
        self.text = text
        self.callback_data = callback_data
        self.url = url
        logger.debug(f"Created button: {text}")

    def to_dict(self) -> Dict:
        result = {"text": self.text}
        if self.callback_data:
            result["callback_data"] = self.callback_data
        if self.url:
            result["url"] = self.url
        return result

class InlineKeyboard:
    def __init__(self):
        self.buttons: List[List[InlineButton]] = []

    def add_row(self, *buttons: InlineButton):
        if not buttons:
            raise TeamXError("At least one button required in row")
        self.buttons.append([btn.to_dict() for btn in buttons])
        logger.debug("Added row to inline keyboard")

    def to_dict(self) -> Dict:
        return {"inline_keyboard": self.buttons}
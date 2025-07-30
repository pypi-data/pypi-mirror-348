from typing import List, Dict
import logging
from .errors import TeamXError

logger = logging.getLogger("TeamXBot.Keyboard")

class ReplyButton:
    def __init__(self, text: str):
        if not text:
            raise TeamXError("Button text cannot be empty")
        self.text = text
        logger.debug(f"Created reply button: {text}")

    def to_dict(self) -> Dict:
        return {"text": self.text}

class ReplyKeyboard:
    def __init__(self, resize: bool = True, one_time: bool = False):
        self.buttons: List[List[ReplyButton]] = []
        self.resize = resize
        self.one_time = one_time

    def add_row(self, *buttons: ReplyButton):
        if not buttons:
            raise TeamXError("At least one button required in row")
        self.buttons.append([btn.to_dict() for btn in buttons])
        logger.debug("Added row to reply keyboard")

    def to_dict(self) -> Dict:
        return {
            "keyboard": self.buttons,
            "resize_keyboard": self.resize,
            "one_time_keyboard": self.one_time
        }
import json
from typing import List
from .inline_keyboard_button import InlineKeyboardButton

class InlineKeyboardMarkup:
  def __init__(self, inline_keyboard: List[List["types.InlineKeyboardButton"]]):
    self._ = "Nexgram.types.InlineKeyboardMarkup"
    if not isinstance(inline_keyboard, list):
      raise TypeError("Failed to read buttons, you should pass list always!")
    
    for x in inline_keyboard:
      if not isinstance(x, list):
        raise TypeError("Failed to read buttons, you should pass 2 list always!")
      for z in x:
        if not isinstance(z, InlineKeyboardButton):
          raise TypeError("Failed to read buttons, you should always pass 'Nexgram.types.InlineKeyboardButton' object always!")
    
    self.inline_keyboard = inline_keyboard

  def __repr__(self):
    data = {k: v for k, v in self.__dict__.items()}
    return json.dumps(
      data,
      indent=2,
      ensure_ascii=False,
      default=lambda o: o.__dict__ if hasattr(o, "__dict__") else o
    )

  def read(self):
    return json.dumps({
      "inline_keyboard": [
        [{k: v for k, v in button.__dict__.items() if not k.startswith("_")} for button in row]
        for row in self.inline_keyboard
      ]
    })
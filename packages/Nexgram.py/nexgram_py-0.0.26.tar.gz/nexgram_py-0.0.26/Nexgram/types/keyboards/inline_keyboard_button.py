import json

class InlineKeyboardButton:
  def __init__(
    self,
    text,
    url=None,
    callback_data=None,
    callback_game=None,
    user_id: int = None,
    switch_inline_query=None,
    switch_inline_query_current_chat=None,
  ):
    self._ = "Nexgram.types.InlineKeyboardButton"
    self.text = text
    if url:
      self.url = url
    elif callback_data:
      self.callback_data = callback_data
    elif callback_game:
      self.callback_game = callback_game
    elif user_id:
      self.url = f"tg://user?id={user_id}"
    elif switch_inline_query:
      self.switch_inline_query = switch_inline_query
    elif switch_inline_query_current_chat:
      self.switch_inline_query_current_chat = switch_inline_query_current_chat
    else: raise Exception("?.")
  def __repr__(self):
    return json.dumps(self.__dict__, indent=2, ensure_ascii=False)
    
import json
from Nexgram.errors import *

def extract_command(text):
  parts = text.lstrip('/').split()
  return parts if parts else None
  
class Message:
  def __init__(
    self,
    client: "Nexgram.Client",
    id: int,
    from_user: "Nexgram.types.User",
    chat: "Nexgram.types.Chat",
    reply_to_message: "Nexgram.types.Message" = None,
    forward_from: "Nexgram.types.User" = None,
    forward_from_chat: "Nexgram.types.Chat" = None,
    reply_markup: "Nexgram.types.InlineKeyboardMarkup" = None,
    caption: str = None,
    text: str = None
  ):
    from Nexgram.types import User, Chat
    from Nexgram import Client
    
    if not isinstance(from_user, User): raise InvalidObject("You should pass 'Nexgram.types.User' object in 'from_user' argument not others.")
    if not isinstance(client, Client): raise InvalidObject("You should pass 'Nexgram.Client' object in 'client' argument not others")
    
    self._ = "Nexgram.types.Message"
    self.id = id
    self.from_user = from_user
    if not isinstance(chat, Chat): raise InvalidObject("You should pass 'Nexgram.types.Chat' object in 'chat' argument not others.")
    self.chat = chat
    if reply_to_message:
      if not isinstance(reply_to_message, Message):
        raise InvalidObject("You should pass 'Nexgram.Client.Message' object in 'reply_to_message' argument not others")
      self.reply_to_message = reply_to_message
    if forward_from:
      if not isinstance(forward_from, User): raise TypeError("?.")
      self.forward_from = forward_from
    if forward_from_chat:
      if not isinstance(forward_from_chat, Chat): raise TypeError("?.")
      self.forward_from_chat = forward_from_chat
    if caption: self.caption = caption
    if text:
      self.text = text
      self.command = extract_command(text)
    self.client = client  
  def __repr__(self):
    from Nexgram import Client
    mf = {"client"}
    def clean(obj):
      if isinstance(obj, Client):
        return None
      if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items() if k not in mf}
      if hasattr(obj, "__dict__"):
        return {
          k: clean(v)
          for k, v in obj.__dict__.items()
          if k not in mf and not callable(v)
        }
      return obj
    return json.dumps(clean(self), indent=2, ensure_ascii=False).replace("\\n", "\n")    
  async def reply(self, text: str, reply_markup = None,parse_mode: str = None):
    client = self.client
    return await client.send_message(
      chat_id=self.chat.id,
      text=text,
      reply_markup=reply_markup,
      reply_to_message_id=self.id,
      parse_mode=parse_mode,
    )
  async def delete(self):
    client, api, url = self.client, self.client.api, self.client.ApiUrl
    return await api.post(url+"deleteMessage", {"chat_id": self.chat.id, "message_id": self.id})
  
  async def forward(self, chat_id):
    client, api, url = self.client, self.client.api, self.client.ApiUrl
    return await client.forward_messages(chat_id, self.chat.id, self.id)
  
  async def copy(self, chat_id, caption=None, parse_mode=None):
    client, api, url = self.client, self.client.api, self.client.ApiUrl
    return await client.copy_messages(chat_id, self.chat.id, self.id, caption=caption, parse_mode=parse_mode)
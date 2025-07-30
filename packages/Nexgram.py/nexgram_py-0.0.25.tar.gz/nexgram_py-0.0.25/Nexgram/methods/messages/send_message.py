import aiohttp
from Nexgram.errors import BadRequest
from Nexgram.types import InlineKeyboardMarkup, Message

class sendMessage:
  async def send_message(
    self,
    chat_id,
    text,
    reply_markup: "Nexgram.types.InlineKeyboardMarkup" = None,
    reply_to_message_id: int = None,
    parse_mode=None,
  ) -> Message:
    if not self.connected: raise ConnectionError("Client is not connected, you must connect the client to send message.")
    url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    data = {"chat_id": chat_id,"text": text}
    if parse_mode:
      data["parse_mode"] = parse_mode
    if reply_to_message_id:
      data["reply_to_message_id"] = reply_to_message_id
    if reply_markup:
      if not isinstance(reply_markup, InlineKeyboardMarkup):
        raise TypeError("You should pass 'Nexgram.types.InlineKeyboardMarkup' in reply_markup not others!")
      data['reply_markup'] = reply_markup.read()
    z = await self.api.post(url,json=data)
    if not z.get('ok') and z.get('error_code'):
      error_type = z.get('description')
      error = z.get('description').split(':', 1)[1]
      if 'bad request' in error_type.lower():
        raise BadRequest(error)
    return await self.create_object(z.get('result'))
from Nexgram.errors import BadRequest
import asyncio

class CopyMessages:
  async def copy_messages(self, chat_id: int, from_chat_id: int, id, caption=None, parse_mode=None):
    if not self.connected: raise ConnectionError("Client is not connected, you must connect the client to copy message.")
    if isinstance(id, int): id = [id]
    output = []
    for x in id:
      if not isinstance(x, int) or not str(x).isdigit():
        raise TypeError("You should only pass integer in message_id")
      if output: asyncio.sleep(0.200)
      data = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": int(x)
      }
      if caption: data['caption'] = caption
      if parse_mode: pass
      z = await self.api.post(self.ApiUrl+"copyMessage", json=data)
      if not z.get('ok') and z.get('error_code'):
        error_type = z.get('description')
        error = z.get('description').split(':', 1)[1]
        if 'bad request' in error_type.lower():
          raise BadRequest(error)
      output.append(z)
    return output
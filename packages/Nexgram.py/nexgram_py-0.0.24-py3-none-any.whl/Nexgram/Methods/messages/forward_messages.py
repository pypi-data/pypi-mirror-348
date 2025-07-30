from Nexgram.errors import BadRequest
import asyncio

class ForwardMessages:
  async def forward_messages(self, chat_id: int, from_chat_id: int, id):
    if not self.connected: raise ConnectionError("Client is not connected, you must connect the client to forward message.")
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
      z = await self.api.post(self.ApiUrl+"forwardMessage", json=data)
      if not z.get('ok') and z.get('error_code'):
        error_type = z.get('description')
        error = z.get('description').split(':', 1)[1]
        if 'bad request' in error_type.lower():
          raise BadRequest(error)
      output.append(z)
    return output

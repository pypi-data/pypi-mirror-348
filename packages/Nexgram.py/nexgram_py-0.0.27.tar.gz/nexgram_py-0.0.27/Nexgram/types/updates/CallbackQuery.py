import json

class CallbackQuery:
  def __init__(
    self,
    client: "Nexgram.Client",
    id: int,
    from_user: "Nexgram.types.User",
    message: "Nexgram.types.Message" = None,
    data: str = None,
  ):
    from Nexgram.types import User, Message
    if not isinstance(from_user, User):
      raise Exception("Cry now i won't say what exception is this")
    elif message and not isinstance(message, Message):
      raise Exception("Cry now i won't say what exception is this")
    self._ = "Nexgram.types.CallbackQuery"
    self.id = id
    self.from_user = from_user
    self.message = message if message else None
    self.data = data
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
  async def answer(self, text: str, show_alert: bool = False, cache_time: int = 0):
    client, api, url = self.client, self.client.api, self.client.ApiUrl
    data = {
      "callback_query_id": self.id,
      "text": text,
      "show_alert": show_alert,
      "cache_time": cache_time,
    }
    return await api.post(url+"answerCallbackQuery", data)
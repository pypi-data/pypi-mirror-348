import json

class ChatJoinRequest:
  def __init__(
    self,
    client: "Nexgram.Client",
    from_user: "Nexgram.types.User",
    chat: "Nexgram.types.Chat",
  ):
    from Nexgram.types import User, Chat
    if not isinstance(from_user, User):
      raise Exception("Cry now i won't say what exception is this")
    elif not isinstance(chat, Chat):
      raise Exception("Cry now i won't say what exception is this")
    self._ = "Nexgram.types.ChatJoinRequest" 
    self.id = id
    self.chat = chat
    self.from_user = from_user
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
    
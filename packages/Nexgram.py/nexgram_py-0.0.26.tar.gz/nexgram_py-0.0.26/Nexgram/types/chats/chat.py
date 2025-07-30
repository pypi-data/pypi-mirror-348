import json

class Chat:
  def __init__(
    self,
    id: int,
    title: str = None,
    first_name: str = None,
    last_name: str = None,
    type: str = None,
    username: str = None,
  ):
    self._ = "Nexgram.types.Chat"
    self.id = id
    if not title:
      if not first_name: 
        raise Exception("You didn't passed title or first_name, you should pass any of them.")
      self.first_name = first_name
      self.last_name = last_name
    else: self.title = title
    self.type = type
    if username: self.username = username
  
  def __repr__(self):
    return json.dumps(self.__dict__, indent=2, ensure_ascii=False)
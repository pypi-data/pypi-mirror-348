from Nexgram.filters import Filter
from Nexgram import filters as f

class OnMessage:
  def on_message(self, filters=None):
    if not isinstance(filters, Filter) and not filters is None:
      filters = f.create(filters)  

    def decorator(mano):
      if mano in self.on_message_listeners:
        raise Exception("You have already used this same decorator, you cannot use it multiple times!")
      self.on_message_listeners[mano] = filters if isinstance(filters, Filter) else None
      return mano
    return decorator

  
from Nexgram.filters import Filter
from Nexgram import filters as f

class OnCallbackQuery:
  def on_callback_query(self, filters=None):
    if not isinstance(filters, Filter) and not filters is None:
      filters = f.create(filters)  

    def decorator(mano):
      if mano in self.on_callback_query_listeners:
        raise Exception("You have already used this same decorator, you cannot use it multiple times!")
      self.on_callback_query_listeners[mano] = filters if isinstance(filters, Filter) else None
      return mano
    return decorator
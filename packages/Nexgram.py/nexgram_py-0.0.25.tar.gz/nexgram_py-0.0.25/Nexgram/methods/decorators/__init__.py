from .on_disconnect import OnDisconnect
from .on import On
from .on_message import OnMessage
from .on_callback_query import OnCallbackQuery
from .on_inline_query import OnInlineQuery

class Decorators(
  On,
  OnDisconnect,
  OnMessage,
  OnCallbackQuery,
  OnInlineQuery,
):
  pass
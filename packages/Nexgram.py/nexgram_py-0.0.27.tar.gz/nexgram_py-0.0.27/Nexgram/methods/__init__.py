from .messages import Messages
from .decorators import Decorators
from .utilities import Utilities
from .chats import Chats

class Methods(
  Messages,
  Utilities,
  Decorators,
  Chats
):
  pass
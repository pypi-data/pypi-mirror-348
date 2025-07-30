from .dispatch_update import Dispatch
from .call import Call
from .create_object import CreateObject
from .stop import Stop
from .start import Start
from .start_polling import StartPolling
from .webhook import Webhook

class Utilities(
  Dispatch,
  Call,
  CreateObject,
  Stop,
  Start,
  StartPolling,
  Webhook
):
  pass
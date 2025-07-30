from .send_message import sendMessage
from .forward_messages import ForwardMessages
from .copy_messages import CopyMessages

class Messages(
  sendMessage,
  ForwardMessages,
  CopyMessages,
):
  pass
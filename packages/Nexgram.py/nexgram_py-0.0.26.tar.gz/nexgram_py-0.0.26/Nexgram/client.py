import logging
import httpx
import aiohttp
import asyncio
from .methods import *
from .errors import *
from .types import *
from .api import Api

log = logging.getLogger(__name__)
clients = []

class Client(Methods):
  def __init__(
    self,
    name: str,
    bot_token: str,
    plugins: str = None,
    avoid_connection_error_stop: bool = True,
  ):
    """
    Nexgram.py - Client
    
    Parameters:
    - name: str (string)
    -- Name of your client.
    - bot_token: str (string)
    -- BotToken is used to connect with your bot. You can create a bot and get its token from t.me/BotFather.
    - plugins: str (string)
    -- path of your plugins folder. It'll run every python files in that folder so you don't need to import everything one by one.
    - avoid_connection_error_stop: bool (boolean)
    -- If its True your client won't stop because of connection errors it'll log it and retry polling.
    """
    self.name = name
    self.bot_token = bot_token
    self.connected = False
    self.me = None
    self.offset = 0
    self.polling = False
    self.ApiUrl = f"https://api.telegram.org/bot{self.bot_token}/"
    self.api = Api()
    self.log = log
    self.mode = None
    clients.append(self)
    self.plugins = plugins
    # Decorators --
    self.on_message_listeners = {}
    self.on_disconnect_listeners = {}
    self.on_callback_query_listeners = {}
    self.on_inline_query_listeners = {}
    self.on_listeners = {}
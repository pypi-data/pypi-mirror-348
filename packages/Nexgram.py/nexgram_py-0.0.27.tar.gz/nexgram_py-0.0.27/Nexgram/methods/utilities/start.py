from Nexgram.types import *
import asyncio
from Nexgram.import_all import import_all

modes = ['polling', 'webhook', 'none']

class Start:
  async def start(
    self,
    mode: str = 'polling',
    webhook_url: str = None,
    webhook_port: int = None,
  ):
    api, url, log = self.api, self.ApiUrl+"getMe", self.log
    if mode.lower() not in modes:
      raise ValueError(f"Mode must be 'polling' or 'webhook' not '{mode}'")
    self.mode = mode.lower()
    if self.plugins:
      import_all(self.plugins)
    r = await api.get(url)
    if r.get("ok"):
      self.connected = True,r = r["result"]
      self.me = User(client=self,id=r['id'],first_name=r['first_name'],username=r['username'],is_self=True,is_bot=True)
      log.info(f"Client connected as {self.me.first_name} (@{self.me.username})")
      if mode=='polling' and True:
        await api.post(self.ApiUrl+"deleteWebhook")
        asyncio.create_task(self.start_polling())
      elif mode == "webhook":
        if not webhook_url or not webhook_port:
          raise ValueError("you selected 'webhook' mode. then where is url & port? you should provid it.")
        if webhook_url.endswith('/'): webhook_url = webhook_url[:-1]
        self.webhook_url, self.webhook_port = webhook_url, webhook_port
        loop = asyncio.get_event_loop()
        loop.create_task(self.createWebhook())
      else:
        raise ValueError(f"Invalid start mode-> {mode}, currently 'polling' and 'webhook' are only supported.")
      return self.me
    raise ValueError("Failed to connect with your bot token. Please make sure your bot token is correct.")
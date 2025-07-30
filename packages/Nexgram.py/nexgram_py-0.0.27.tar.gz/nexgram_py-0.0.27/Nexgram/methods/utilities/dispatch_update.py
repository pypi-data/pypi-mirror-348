from Nexgram.errors import *
from Nexgram.types import *
import asyncio

class Dispatch:
  async def __dispatch_helper(self, src, update, update_type='message'):
    try:
      m = update.get(update_type)
      message = await self.create_object(m,update_type)
      for x in src:
        asyncio.create_task(self.call(src, x, self, message))
    except Exception as e:
      self.log.error(f"[DispatchUpdate] Line 13: {e}")
  
  async def dispatch_update(self, update):
    log = self.log
    for gf in self.on_listeners:
      asyncio.create_task(gf(update))
    if update.get('message'):
      update_type, src = "message", self.on_message_listeners
      await self.__dispatch_helper(src=src,update=update,update_type=update_type)
    elif update.get("callback_query"):
      update_type, src = "callback_query", self.on_callback_query_listeners
      await self.__dispatch_helper(src=src,update=update,update_type=update_type)
    elif update.get("inline_query"):
      update_type, src = "inline_query", self.on_inline_query_listeners
      await self.__dispatch_helper(src=src,update=update,update_type=update_type)
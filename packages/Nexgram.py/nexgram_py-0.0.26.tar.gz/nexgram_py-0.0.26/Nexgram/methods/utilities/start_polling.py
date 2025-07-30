import asyncio
from Nexgram.errors import *

class StartPolling:
  async def start_polling(self):
    if not self.connected:
      raise ConnectionError("Client is not connected. Please connect the client and start polling.")
    elif self.polling: raise PollingAlreadyStartedError("Polling already started, why you trying again and again? didn't you receive any updates?")
    self.polling, log = True, self.log
    log.info("Nexgram.py - polling started!")
    first_start = True
    max_retry, retry = 25, 1
    while self.polling:
      try:
        params = {"offset": self.offset, "timeout": 15}
        updates = await self.api.get(self.ApiUrl+"getUpdates", params=params)
        if "result" in updates and not first_start:
          for update in updates["result"]:
            self.offset = update["update_id"] + 1
            asyncio.create_task(self.dispatch_update(update))
        elif "result" in updates and first_start:
          first_start = False
        elif 'error_code' in updates:
          err = updates.get('description')
          code = int(updates.get('error_code'))
          if code == 401:
            raise BadRequest(f"Telegram says: [{code}_{err.upper()}] - The bot token you provied is incorrect or revoked (caused by 'Client.start_polling')")
      except Exception as e:
        if self.avoid_connection_error_stop and retry > max_retry:
          log.info("Stopping clients.")
          break
        if self.avoid_connection_error_stop: log.error(f"[{retry}] Error in polling: {e}")
        else: log.error(f"[{retry}/{max_retry}] Error in polling: {e}")
        retry += 1
    await self.stop()
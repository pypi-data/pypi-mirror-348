class Stop:
  async def stop(self):
    await self.trigger_disconnect()
    self.polling,self.connected=False,False
    self.log.info("Client stopped.")
import aiohttp

class Api:
  async def post(self, url, json: dict = None, need_text=False):
    async with aiohttp.ClientSession() as mano:
      async with mano.post(url=url, json=json) as ily:
        if need_text:
          return await ily.text()
        else: return await ily.json()

  async def get(self, url, params=None, need_text=False):
    async with aiohttp.ClientSession() as mano:
      async with mano.get(url=url, params=params) as ily:
        if need_text:
          return await ily.text()
        else: return await ily.json()
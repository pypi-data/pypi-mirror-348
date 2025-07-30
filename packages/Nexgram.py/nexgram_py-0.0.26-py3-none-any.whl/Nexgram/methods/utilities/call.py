import asyncio
import inspect

class Call:
  async def call(self, src, func, *args):
    if func not in src: return
    filter_func = src.get(func)
    if filter_func:
      if inspect.iscoroutinefunction(filter_func.func):
        passed = await filter_func(*args)  
      else:
        passed = await asyncio.to_thread(filter_func.func, *args)
      if passed: await func(*args)
    else: await func(*args)
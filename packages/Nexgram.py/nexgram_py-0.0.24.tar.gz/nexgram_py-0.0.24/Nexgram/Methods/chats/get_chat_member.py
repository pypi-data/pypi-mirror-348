from Nexgram.types import User
from Nexgram.errors import *

class GetChatMember:
  async def get_chat_member(self, chat_id: int, user_id: int):
    api, log, url = self.api, self.log, self.ApiUrl
    d = {"chat_id": chat_id, "user_id": user_id}
    r = await api.post(url+"getChatMember", d)
    if r.get('ok') and r.get('result'):
      user = r['result']['user']
      return r
      return User(
        client=self,
        id=user.get('id'),
        first_name=user.get('first_name'),
        last_name=user.get('last_name'),
        username=user.get('username'),
        is_bot=user.get('is_bot'),
      )
    return False
    if not r.get('ok') and r.get('error_code'):
      error_type = r.get('description')
      error = r.get('description').split(':', 1)[1]
      if 'bad request' in error_type.lower():
        raise BadRequest(error)
    # incompleted
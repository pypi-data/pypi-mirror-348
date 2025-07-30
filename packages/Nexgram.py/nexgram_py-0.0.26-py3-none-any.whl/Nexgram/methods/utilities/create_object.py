from Nexgram.types import *

class CreateObject:
  async def create_object(self, data, object_type='message'):
    user_fields = ['id', 'first_name', 'last_name', 'username', 'is_bot']
    chat_fields = ['id', 'title', 'first_name', 'last_name', 'type', 'username']
    
    def create_user(data):
      return User(client=self, **{key: data.get(key) for key in user_fields})   
    def create_chat(data):
      return Chat(**{key: data.get(key) for key in chat_fields})
    
    from_user = data.get('from_user') or data.get('from')
    chat = data.get('chat')
    callback_query_message = data.get('message')
    forward_from = data.get('forward_from')
    forward_from_chat = data.get('forward_from_chat')
    
    if from_user:
      from_user = create_user(from_user)
    if chat:
      chat = create_chat(chat)
    if callback_query_message:
      callback_query_message = await self.create_object(callback_query_message)
    if forward_from:
      forward_from = create_user(forward_from)
    if forward_from_chat:
      forward_from_chat = create_chat(forward_from_chat)
    
    object_mapping = {
      'message': Message(
        client=self,
        id=data.get('message_id') or data.get('id'),
        from_user=from_user,
        chat=chat,
        forward_from=forward_from,
        forward_from_chat=forward_from_chat,
        reply_markup=None,
        caption=data.get('caption'),
        text=data.get('text'),
      ),
      'callback_query': CallbackQuery(
        client=self,
        id=data.get('id'),
        from_user=from_user,
        message=callback_query_message,
        data=data.get('data')
      ),
      'inline_query': InlineQuery(
        client=self,
        id=data.get('id'),
        from_user=from_user,
        query=data.get('query'),
        offset=data.get('offset')
      )
    }    
    return object_mapping.get(object_type)
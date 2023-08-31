import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from chat.models import Thread, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        

        if not msg:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        count = await self.get_thread_messages_count(thread_id)
        sender_img = await self.get_sender_img(sent_by_id)
        reciver_img = await self.get_reciver_img(send_to_id)
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        timestamp =await self.create_chat_message(thread_obj, sent_by_user, msg)
        date_str = timestamp.strftime('%d %a')
        time_str = timestamp.strftime('%H:%M')

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id,
            'count': count,
            'sender_img': sender_img,
            'reciver_img': reciver_img,
            'date_str': date_str,
            'time_str':time_str
           
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )



    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
    
    @database_sync_to_async
    def get_sender_img(self, user_id):
        qs = User.objects.get(id=user_id).profile.image.url
        return qs
    
    @database_sync_to_async
    def get_reciver_img(self, user_id):
        qs = User.objects.get(id=user_id).profile.image.url
        return qs

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
    
    @database_sync_to_async
    def get_thread_messages_count(self, thread_id):
        qs = Thread.objects.get(id=thread_id).chatmessage_thread.count()
        return qs+1

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        message = ChatMessage.objects.create(thread=thread, user=user, message=msg)
        timestamp = message.timestamp
        return timestamp

import base64
import json
import secrets
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from users.models import MyUser
from chat.models import Message
from users.models import CustomUser
from asgiref.sync import sync_to_async





class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user:CustomUser = self.scope["user"]

        if user.is_authenticated:
            

            self.room_name = user.generate_room(self.scope["url_route"]["kwargs"]["room_name"])
            
            self.room_group_name = f"chat_{self.room_name}"
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )

            


            # send to group
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    'type':'tester_message',
                    'tester':'tester'
                }
            )

            await self.accept()
        else:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            

            await self.close()
            


    async def tester_message(self,event):
        tester = event['tester']
        

        await self.send(text_data=json.dumps({
            'tester':tester
        }))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        room = self.room_name
        sender:CustomUser = self.scope["user"]

        try:
            receiver:CustomUser = await sync_to_async(sender.get_receiver)(room)
        except CustomUser.DoesNotExist:
            await self.close()

        # unpack the dictionary into the necessary parts
        message = text_data_json["message"]

        
        _message:Message = await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            body=message,
            room=room
        )
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "status": _message.status,
                "created_at": str(_message.created_at),
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": event["sender"],
                    "status": event["status"],
                    "created_at": event["created_at"],
                }
            )
        )
    
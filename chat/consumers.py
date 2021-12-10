import base64
import json
import secrets
from datetime import datetime
from typing import Any, Dict
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from users.models import MyUser
from chat.models import Message
from users.models import CustomUser
from asgiref.sync import sync_to_async





class ChatRoomConsumer(AsyncWebsocketConsumer):
    allowed_events = ("new_message","read_message","ping")
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
            # await self.channel_layer.group_send(
            #     self.room_group_name, 
            #     {
            #         'type':'tester_message',
            #         'tester':'tester'
            #     }
            # )

            await self.accept()
        else:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            

            await self.close()
            


    # async def tester_message(self,event):
    #     tester = event['tester']
        

    #     await self.send(text_data=json.dumps({
    #         'tester':tester
    #     }))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        # unpack the dictionary into the necessary parts
        payload = text_data_json.get("payload") or {}
        event = (text_data_json.get("event") or '').lower()

        
        
        # prevent frontend from trigerring restricted event if any
        if not event in self.allowed_events:return 
        
        
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": f"on_{event}",
                "payload": payload
            },
        )


    async def get_event_data(self,event_:Dict[str,Any]):
        event:str = event_["type"].replace("on_",'')
        payload = event_["payload"] or {}

        return event,payload


    async def emit(self,event,**kwargs):
        
        await self.send(
            text_data=json.dumps(
                {
                    "event": event.upper(),
                    "payload": kwargs,
                
                }
            )
        )


    # Receive message from room group
    async def on_read_message(self, event):
        event,payload = await self.get_event_data(event)

        message_id = payload.get("message_id")
        

        try:
            message:Message = await sync_to_async(Message.objects.get)(
                receiver=self.scope["user"],
                id=int(message_id),
                active = True
            )
            await sync_to_async(message.read)()
        except Message.DoesNotExist:
            return
        except Exception as e:
            print(e)
            return 

        # Send message to WebSocket
        await self.emit(
            event,
            id = message.id,
            body = message.body,
            status = message.status,
            created_at = str(message.created_at)
        )
        
    


    # Receive message from room group
    async def on_new_message(self, event):
        event,payload = await self.get_event_data(event)

        message = payload.get("message")
        room = self.room_name

        if not message:return

        sender:CustomUser = self.scope["user"]

        try:
            receiver:CustomUser = await sync_to_async(sender.get_receiver)(room)
        except CustomUser.DoesNotExist:
            await self.close()


        _message_obj:Message = await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            body=message,
            room=room
        )
       

        # Send message to WebSocket
        await self.emit(
            event,
            id = _message_obj.id,
            message = message,
            sender = sender.id,
            status = _message_obj.status,
            created_at = str(_message_obj.created_at),
        )

    async def on_ping(self,event):
        event,payload = await self.get_event_data(event)
        
        await self.send(text_data=json.dumps({
            'message': "pong"
        }))


    
        

        
    
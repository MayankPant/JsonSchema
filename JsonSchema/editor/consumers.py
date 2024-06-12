import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from .models import User, Schema
from .views import *
from .serializers import UserSerializer


class VerificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #create a unique group name based on the user
        self.group_name = "user_info"
        print(self.channel_name)
        print(self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print("WebSocket connection accepted and added to group")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket connection closed and removed from group")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received data from WebSocket:", data)
        if data.get("event") == "SAVE":
            del data['event']
            await self.save_schema(data)
        elif data.get("event") == "DELETE":
            del data['event']
            await self.delete_schema(data)

        
    async def send_user_data_event(self, event):
        print("Type: ", event['type'])
        data = event['data']
        print("Sending data to WebSocket:", data)
        await self.send(text_data=json.dumps(data))

    async def save_schema(self, data):
        user = await self.get_user()
        print(UserSerializer(user).data)
        if user != None:
            new_schema = await self.query_save_schema(user, data)
            print("Saved schema ")
        else:
            print("No logged in user")


            
    async def delete_schema(data):
        pass

    @database_sync_to_async
    def get_user(self):
        user_id = self.scope["session"].get('user_id')
        print(user_id)
        if user_id != None:
            try:    
                return User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return None
        return None
    
    @database_sync_to_async
    def query_save_schema(self, user, data):
        new_schema = Schema(user=user, schema_name=data['schemaName'], schema_text=data['schema'])
        new_schema.save()
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from .models import User, Schema
from .views import *
from .serializers import UserSerializer, SchemaSerializer
from .utils import JsonSchemaValidator


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


        elif data.get("type") == "websocket_acknowledgement":
            user = await self.get_user()
            if user != None:
                user_data = UserSerializer(user).data
                user_schemas = self.scope["session"].get("user_schemas")
                relevant_user_data = {
                    "user" : user_data,
                    "user_schemas" : user_schemas
                }
                await self.send_user_data({"event" : "send_user_data_event", "user_data" : relevant_user_data})
        
        elif data.get("event") == "DELETE":
            del data['event']
            await self.delete_schema(data)


        elif data.get("event") == "editor_change":
            schema = data["schema"]
            user_input = data["user_input"]
            if JsonSchemaValidator.validate_jsonschema(self, schema):
                if JsonSchemaValidator.validate(self, schema, user_input):
                    return await self.send(json.dumps({"event" : "editor_change", "Validation":"True"}))
            return await self.send(json.dumps({"event" : "editor_change", "Validation":"False"}))



    @database_sync_to_async
    def get_user_schemas(self, user: User):
        try:
            user_schemas = Schema.objects.filter(user=user)
            return user_schemas
        except Schema.DoesNotExist:
            return None


    async def send_user_data(self, event):
        print("Type: ", event['event'])
        data = event['user_data']
        print("Sending data to WebSocket:", data)
        await self.send(text_data=json.dumps(event))

    async def save_schema(self, data):
        user = await self.get_user()
        print(UserSerializer(user).data)
        if user != None:
            new_schema = await self.query_save_schema(user, data)
            user_schemas = await self.get_user_schemas(user)
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
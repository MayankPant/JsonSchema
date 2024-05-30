import json
from channels.generic.websocket import AsyncWebsocketConsumer
from validate import validate

class VerificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print("Websocket disconnected!")

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Verify the data (simple check for this example)
        if validate(data):
            response = 'Data is verified'
        else:
            response = 'Invalid data'

        await self.send(text_data=json.dumps({
            'response': response
        }))

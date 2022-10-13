import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notification'
        #rejoindre le groupe
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        #quitter le groupe
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    #recevoir les messages du socket

    async def receive(self, text_data):
        text_data_json =  json.loads(text_data)
        message = text_data_json['message']

        event = {
            'type':'send_message',
            'message': message,

        }
        #envoyer le message au groupe
        await self.channel_layer.group_send(self.group_name, event)

        #envoyer le message au web socket
        await self.send(text_data=json.dumps({'message':message}))

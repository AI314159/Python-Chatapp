import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Server, Message
from django.contrib.auth.models import User
from .commands import interpret_cmd

@database_sync_to_async
def add_message(server_id, username, message):
    server = Server.objects.get(id=server_id)
    user = User.objects.get(username=username)
    msg = Message(server=server, sender=user, contents=message)
    msg.save()

@database_sync_to_async
def get_role(server_id, username):
    server = Server.objects.get(id=server_id)
    user = User.objects.get(username=username)
    if server.owner.username == username:
        return "owner"
    elif user in server.moderators.all():
        return "mod"
    elif user in server.admins.all():
        return "admin"
    else:
        return None

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = self.room_name
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data["message"]
        username = json_data["username"]
        print(json_data)

        await interpret_cmd(message, username, self.room_name)
        await add_message(self.room_name, username, message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send_message",
                "message": message,
                "username": username
            }
        )

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({
            "message": message, 
            "username": username, 
            "role": await get_role(self.room_name, username)}))

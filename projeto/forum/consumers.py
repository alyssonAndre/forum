import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Define o ID do post e o nome do grupo
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'post_{self.post_id}'

        # Entra no grupo do post
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code=None):
        # Sai do grupo ao desconectar
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Recebe e trata a mensagem enviada pelo cliente
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        # Envia a mensagem para o grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        # Envia a mensagem para o WebSocket do cliente
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

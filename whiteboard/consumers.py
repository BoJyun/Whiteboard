from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import logging
from time import sleep

# logging module with django logging
logger = logging.getLogger('django')

class ChatConsumer(WebsocketConsumer):
   def connect(self):
        # self.name = self.scope['url_route']['kwargs']['name']
        # self.room_group_name="sg24"
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        self.accept()
        asd.get()
        print(asd)
        for i in range(1,10):
            self.send(text_data=json.dumps({
            'message': i
            }))
            sleep(1)

    # async def disconnect(self, close_code):
    #     pass

    # async def receive(self,asd):
    #     # text_data_json = json.loads(text_data)
    #     # message = self.name + ': ' + text_data_json['message']
    #     # logger.debug('send')

    #     self.send(text_data=json.dumps({
    #         'message': asd
    #     }))
# https://stackoverflow.com/questions/53461830/send-message-using-django-channels-from-outside-consumer-class\
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # def chat_message(self, event):
    #     message = event['message']
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))
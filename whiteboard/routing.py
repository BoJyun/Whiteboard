from django.urls import path
from .views import ChatConsumer

websocket_urlpatterns = [
    path('whiteboard/ws/chat/', ChatConsumer.as_asgi()),
]
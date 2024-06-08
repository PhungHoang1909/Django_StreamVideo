from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video/<str:group_name>/', consumers.VideoConsumer.as_asgi()),
]

from django.urls import re_path # a function allow using regular expression to match URL pattern

from . import consumers

# A list that holds URls patterns for Websockets connection.
# Used by ASGI app to route incoming websockets connections to approriate consumer
websocket_urlpatterns = [
    re_path(r'', consumers.ChatConsumer.as_asgi()),
]
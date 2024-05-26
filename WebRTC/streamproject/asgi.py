import os # Interact with operating system (setting environment variables)

from channels.routing import ProtocolTypeRouter, URLRouter # Used to route different types of protocol request(HTTP and Websocket)
from django.core.asgi import get_asgi_application # get default asgi app for handle websockets connect
from channels.auth import AuthMiddlewareStack # middleware to handle authenticaiton for websocket connect
import streamapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings') # default settings
django_asgi_app = get_asgi_application()

# Define the ASGI app
application = ProtocolTypeRouter({
    "http": django_asgi_app, # HTTP Request: Route to django_asgi_app (handle HTTP requests)

    # Websocket request: manager user authentication
    "websocket": AuthMiddlewareStack(
        URLRouter(
            streamapp.routing.websocket_urlpatterns # route based on the url patterns defined 
        )
    )
})
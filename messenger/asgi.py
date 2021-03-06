
import os

# from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')



from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat import routing
from messenger.auth import QueryAuthMiddleware


asgi_application = get_asgi_application()



application = ProtocolTypeRouter({
  "http": asgi_application,
  "websocket": QueryAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
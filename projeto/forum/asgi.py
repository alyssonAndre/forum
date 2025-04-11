import os
from channels.routing import ProtocolTypeRoute, URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import forum.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

application = ProtocolTypeRouter({
    "https": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(forum.routing.websocket_urlpatterns)
    ),
})
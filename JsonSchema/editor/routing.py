from django.urls import path
from .consumers import VerificationConsumer

websocket_urlpatterns = [
    path("ws/verify/", VerificationConsumer.as_asgi()),
]
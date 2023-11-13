from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name_id>\w+)/$", consumers.ChatCustomer.as_asgi()),
    re_path(r"ws/directmessage/(?P<direct_room_id>\w+)/$", consumers.DirectMessage.as_asgi()),
]
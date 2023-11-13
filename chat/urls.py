from django.urls import path, include
from webchat.settings import STATIC_URL
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.GuestView.as_view(), name="register-page"),
    path("login", views.LoginView.as_view(), name="login-page"),
    path('chat/<str:room_name>/', views.room, name="room-url"),
    path('', views.MainChat.as_view()),
    path('convert', views.user_convert, name="convert"),
    path('search/<str:search_query>/', views.search, name="search"),
    path('users/<str:user_name>/', views.users, name="add-friend"),

    path('directmessage/<str:direct_room>/', views.directMessages),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
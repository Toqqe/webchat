from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ActiveRooms, CustomUser, DirectRooms, DirectMessages

# Register your models here.

admin.site.register(ActiveRooms)

admin.site.register(CustomUser)
admin.site.register(DirectRooms)
admin.site.register(DirectMessages)
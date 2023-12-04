
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# from django.conf import settings
import secrets
import string
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    is_guest = models.BooleanField(default=False)
    user_img = models.ImageField(upload_to="user_images", default="blank-usr-img.png")
    friends = models.ManyToManyField('self', blank=True )
    online = models.BooleanField(default=False)


User = get_user_model()   

class ActiveRooms(models.Model):
    name = models.CharField(max_length=50)
    users_online = models.IntegerField(default=0)
    users = models.ManyToManyField(CustomUser, related_name="users", blank=True )

    def __str__(self):
        return self.name
    
class MessagesRoom(models.Model):
    room = models.ForeignKey(ActiveRooms, on_delete=models.CASCADE,null=True )
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="message_author")
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class DirectRooms(models.Model):
    author = models.CharField(max_length=100, default=None)
    friend = models.CharField(max_length=100, default=None)
    users = models.ManyToManyField(User, related_name="direct_users", blank=True)
    default = models.CharField(max_length=4, default='')

    def save(self, *args, **kwargs):
        if not self.default:
            # Generowanie losowych 4 znaków
            random_chars = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            self.default = random_chars
        super().save(*args, **kwargs)


    def __str__(self):
        return self.default
    
class DirectMessages(models.Model):
    room = models.ForeignKey(DirectRooms, on_delete=models.CASCADE,null=True )
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="direct_message_author")
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.name
    
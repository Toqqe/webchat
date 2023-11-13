# Generated by Django 4.1.4 on 2023-10-20 22:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_activerooms_users_activerooms_users_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='activerooms',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]

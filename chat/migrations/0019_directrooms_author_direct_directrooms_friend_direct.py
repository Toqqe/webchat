# Generated by Django 4.1.4 on 2023-11-03 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_directrooms_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='directrooms',
            name='author_direct',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='author_msg', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='directrooms',
            name='friend_direct',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='friend_msg', to=settings.AUTH_USER_MODEL),
        ),
    ]
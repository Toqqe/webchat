# Generated by Django 4.1.4 on 2023-12-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_directrooms_author_alter_directrooms_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='activerooms',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.4 on 2023-10-20 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_activerooms_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activerooms',
            old_name='user',
            new_name='users',
        ),
    ]

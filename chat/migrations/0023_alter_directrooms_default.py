# Generated by Django 4.1.4 on 2023-11-03 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0022_directrooms_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directrooms',
            name='default',
            field=models.CharField(default='', max_length=4),
        ),
    ]
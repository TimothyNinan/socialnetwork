# Generated by Django 3.0.8 on 2020-07-28 17:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200728_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='following',
            name='following',
        ),
        migrations.AddField(
            model_name='following',
            name='followee',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]

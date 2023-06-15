from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.IntegerField(default=0)

class Posts(models.Model):
    poster = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField()
    likes = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField(User)

class Following(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="follower")
    followee = models.ManyToManyField(User)
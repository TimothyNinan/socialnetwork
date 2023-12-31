
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("posts/<int:post_id>", views.edit, name="edit"),
    path("likes/<int:post_id>", views.like, name="like"),
    path("<str:username>", views.profile, name="profile")
]

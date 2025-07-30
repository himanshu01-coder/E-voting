from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login, name="login"),  # Homepage opens login page
    path("index/", views.index, name="index"),
    path("vote/", views.vote, name="vote"),
    path("result/", views.result, name="result"),
    path("profile/", views.profile, name="profile"),
    path("vote1/", views.vote1, name="vote1"),
    path("vote2/", views.vote2, name="vote2"),
    path("vote3/", views.vote3, name="vote3"),
    path("confirm/", views.confirm, name="confirm"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"), 
    path("fpass/", views.fpass, name="fpass"),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from journale.wenyeji.views import (
    UserViewset, user_register, user_login, user_logout
)

userRouter = DefaultRouter()
userRouter.register("", UserViewset, basename="users")


urlpatterns = [
    path("register", user_register, name="register"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
]
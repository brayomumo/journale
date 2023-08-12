from django.urls import path, include
from rest_framework.routers import DefaultRouter

from journale.wenyeji.views import UserViewset

userRouter = DefaultRouter()
userRouter.register("", UserViewset, basename="users")

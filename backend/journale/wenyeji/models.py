from django.db import models
from django.contrib.auth.models import AbstractUser

from journale.common.models import BaseModel

# Create your models here.
class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    
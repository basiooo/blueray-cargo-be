from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.managers import UserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

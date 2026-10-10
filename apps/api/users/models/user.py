import random
import string
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=128, unique=True)

    # contact information fields
    email = models.EmailField(unique=True, null=False, blank=False)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # personal information fields
    display_name = models.CharField(max_length=255, default="", blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # avatar field
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    # status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # tracking fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

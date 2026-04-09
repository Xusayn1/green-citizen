import logging

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.shared.models import BaseModel

logger = logging.getLogger(__name__)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user model with flexible authentication fields
    """

    phone_number = models.CharField(
        max_length=20, unique=True, db_index=True,
        null=True, blank=True
    )
    email = models.EmailField(
        max_length=255, unique=True, null=True,
        blank=True, db_index=True
    )

    username = models.CharField(
        max_length=150, unique=True, null=True,
        blank=True, db_index=True
    )

    # Profile fields
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=64, blank=True, null=True)

    # Status fields
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # This field is used for authentication
    USERNAME_FIELD = 'username'  # Default to username, but can authenticate with any
    REQUIRED_FIELDS = []  # No required fields since we have flexible auth

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
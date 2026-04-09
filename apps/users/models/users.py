import logging

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.shared.models import BaseModel

logger = logging.getLogger(__name__)


class User(AbstractUser, BaseModel):
    """
    Custom user model built on top of Django's AbstractUser with an
    extra phone number and audit fields from BaseModel.
    """

    phone_number = models.CharField(
        max_length=20, unique=True, db_index=True,
        null=True, blank=True
    )

    email = models.EmailField(
        max_length=255, unique=True, null=True,
        blank=True, db_index=True
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

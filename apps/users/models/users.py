from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import BaseModel, Language


class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone_number field must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)

    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=64, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    language = models.CharField(max_length=5, choices=Language.choices, default=Language.EN)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username or self.phone_number or str(self.pk)

    def has_permission(self, codename):
        if self.is_superuser:
            return True

        return self.user_permissions_direct.filter(
            permission__codename=codename,
            is_active=True,
        ).exists()

    def get_tokens(self, access_lifetime=None, refresh_lifetime=None):
        refresh = RefreshToken.for_user(self)

        if access_lifetime:
            refresh.access_token.set_exp(lifetime=access_lifetime)
        if refresh_lifetime:
            refresh.set_exp(lifetime=refresh_lifetime)

        refresh["user_id"] = self.id

        expires_at = timezone.now() + timedelta(
            seconds=refresh.access_token.lifetime.total_seconds()
        )
        refresh_expires_at = timezone.now() + timedelta(
            seconds=refresh.lifetime.total_seconds()
        )

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "token_type": "Bearer",
            "expires_at": expires_at.isoformat(),
            "refresh_expires_at": refresh_expires_at.isoformat(),
        }

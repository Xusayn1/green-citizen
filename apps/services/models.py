from django.contrib.auth import get_user_model
from django.db import models

from apps.services.manager import UserServiceSoftDeleteManager
from apps.shared.models import BaseModel, Media

User = get_user_model()


class UserServiceStatus(models.TextChoices):
    IN_PROGRESS = 'IN_PROGRESS', 'In progress'
    APPROVED = 'APPROVED', 'Approved'
    CANCELED = 'CANCELED', 'Canceled'


class ServiceType(BaseModel):
    title = models.CharField(max_length=255)
    score = models.JSONField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'service_type'
        verbose_name_plural = 'Service types'

    def __str__(self):
        return self.title


class UserService(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='services'
    )
    service_type = models.ForeignKey(
        ServiceType, on_delete=models.PROTECT,
        related_name='user_services'
    )
    status = models.CharField(
        choices=UserServiceStatus.choices,
        default=UserServiceStatus.IN_PROGRESS,
        max_length=20
    )
    # data should always have quantity
    # because I will need that to calculate total score
    # for that user services
    images = models.ManyToManyField(
        Media, related_name='services'
    )
    data = models.JSONField(default=dict)
    score = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    objects = UserServiceSoftDeleteManager()

    class Meta:
        db_table = 'user_services'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['service_type', 'status']),
        ]

    def __str__(self):
        return f"{self.user} - {self.service_type}"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class UserServiceStatusHistory(BaseModel):
    user_service = models.ForeignKey(
        UserService, on_delete=models.CASCADE,
        related_name='status_history'
    )
    # Store user info as text to preserve history even after user deletion
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    old_status = models.CharField(
        choices=UserServiceStatus.choices,
        max_length=20,
        null=True, blank=True  # First status won't have old_status
    )
    new_status = models.CharField(
        choices=UserServiceStatus.choices,
        max_length=20
    )

    class Meta:
        db_table = 'user_service_status_history'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_service', '-created_at']),
        ]
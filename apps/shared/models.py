import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with UUID primary key and timestamp fields
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
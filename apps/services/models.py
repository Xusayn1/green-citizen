from django.db import models
from django.conf import settings


class ServiceType(models.Model):
    """
    Service Type model
    """
    name = models.CharField(max_length=255, unique=True)
    score = models.JSONField(default=dict)

    class Meta:
        db_table = 'service_types'
        verbose_name = 'Service Type'
        verbose_name_plural = 'Service Types'

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Service model
    """
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    data = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    score = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name




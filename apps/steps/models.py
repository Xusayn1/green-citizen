from django.db import models
from django.conf import settings


class Step(models.Model):
    """
    Step model for tracking user steps
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='steps')
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'steps'
        verbose_name = 'Step'
        verbose_name_plural = 'Steps'
        ordering = ['-created_at']

    def __str__(self):
        return f"Step {self.count} for {self.user}"

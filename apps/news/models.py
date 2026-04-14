from django.db import models
from django.conf import settings


class News(models.Model):
    """
    News model for publishing news articles
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    is_published = models.BooleanField(default=True)

    class Meta:
        db_table = 'news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

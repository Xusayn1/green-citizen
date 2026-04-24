from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.news.models import News


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('published_at',)
    ordering = ('-published_at',)

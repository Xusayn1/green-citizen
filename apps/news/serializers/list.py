from rest_framework import serializers

from apps.news.models import News
from apps.shared.serializers import TranslationReadMixin


class NewsListSerializer(TranslationReadMixin, serializers.ModelSerializer):
    translatable_tabs = ['title', 'content']

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_at', 'is_published']

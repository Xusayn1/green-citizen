from rest_framework import serializers

from apps.services.models import ServiceType
from apps.shared.serializers import TranslationReadMixin

class ServiceTypeListSerializer(TranslationReadMixin, serializers.ModelSerializer):
    translatable_tabs = ['title']
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        return obj.score.get(self.context['request'].user.language)

    class Meta:
        model = ServiceType
        fields = ['id', 'title', 'score', 'is_active']
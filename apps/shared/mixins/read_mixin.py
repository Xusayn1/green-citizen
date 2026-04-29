class TranslatedFieldsReadMixin:
    """
    Mixin for GET/LIST serializers
    Returns content in language from request.lang
    """

    def to_representation(self, instance):
        data = super().to_representation(instance)

        translatable_fields = getattr(self, 'translatable_fields', [])
        media_fields = getattr(self, 'media_fields', [])

        request = self.context.get('request')
        lang = self._get_language(request)

        # Handle translatable fields
        for field_name in translatable_fields:
            # Text field
            field_key = f"{field_name}_{lang}"
            if hasattr(instance, field_key):
                value = getattr(instance, field_key, '')
                data[field_name] = value if value else ''

        for field_name in media_fields:
            data[field_name] = self._get_media(instance, field_name, request)

        return data

    @staticmethod
    def _get_language(request):
        from apps.shared.models import Language
        valid = [l[0].lower() for l in Language.choices]

        # 1. Check Accept-Language header
        if request:
            header_lang = request.headers.get('Accept-Language', '').lower().strip()
            if header_lang and header_lang in valid:
                return header_lang

            # 2. Check user's active device language
            user = getattr(request, 'user', None)
            if user and user.is_authenticated:
                from apps.users.models.device import Device
                device = Device.objects.filter(user=user, is_active=True).order_by('-last_login').first()
                if device and device.language:
                    device_lang = device.language.lower()
                    if device_lang in valid:
                        return device_lang

        # 3. Default
        return 'en'

    @staticmethod
    def _get_media(instance, field_name, request):
        media = getattr(instance, field_name, None)
        if media:
            from apps.shared.serializers.media import MediaSmallDetailSerializer
            data = MediaSmallDetailSerializer(media, context={'request': request}).data
            return data
        return None
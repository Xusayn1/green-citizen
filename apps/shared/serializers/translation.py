from django.utils.translation import get_language
from modeltranslation.utils import build_localized_fieldname, resolution_order


class TranslationReadMixin:
    """
    Keep the API surface on base field names (title, content, name, ...)
    while reading translated values from modeltranslation fields.
    """

    translation_languages = ("en", "ru", "uz")
    language_query_param = "lang"

    def get_translatable_fields(self):
        return tuple(
            getattr(self, "translatable_fields", getattr(self, "translatable_tabs", ()))
        )

    def get_requested_language(self):
        request = self.context.get("request")
        raw_language = ""

        if request is not None:
            query_params = getattr(request, "query_params", request.GET)
            raw_language = (
                query_params.get(self.language_query_param)
                or request.headers.get("Accept-Language", "")
            )

        if not raw_language:
            raw_language = get_language() or ""

        language = raw_language.split(",")[0].split(";")[0].strip().replace("_", "-").lower()
        if "-" in language:
            language = language.split("-", 1)[0]

        if language in self.translation_languages:
            return language
        return self.translation_languages[0]

    def get_translation_field_names(self):
        translated_field_names = []
        for field_name in self.get_translatable_fields():
            for language in self.translation_languages:
                translated_field_names.append(build_localized_fieldname(field_name, language))
        return translated_field_names

    def get_field_names(self, declared_fields, info):
        field_names = list(super().get_field_names(declared_fields, info))
        translated_field_names = set(self.get_translation_field_names())
        return [field_name for field_name in field_names if field_name not in translated_field_names]

    def get_translated_value(self, instance, field_name, language):
        for language_code in resolution_order(language):
            localized_field = build_localized_fieldname(field_name, language_code)
            value = getattr(instance, localized_field, None)
            if value not in (None, ""):
                return value
        return getattr(instance, field_name, None)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        language = self.get_requested_language()

        for field_name in self.get_translatable_fields():
            data[field_name] = self.get_translated_value(instance, field_name, language)

        for field_name in self.get_translation_field_names():
            data.pop(field_name, None)

        return data

from modeltranslation.translator import register, TranslationOptions

from apps.services.models import ServiceType


@register(ServiceType)
class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ('title',)
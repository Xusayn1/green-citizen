from modeltranslation.translator import TranslationOptions, register

from apps.services.models import Service, ServiceType


@register(ServiceType)
class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name",)

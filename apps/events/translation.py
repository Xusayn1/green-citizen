from modeltranslation.translator import TranslationOptions, register

from apps.events.models import Event


@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ("title", "description")

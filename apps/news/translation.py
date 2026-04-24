from modeltranslation.translator import TranslationOptions, register

from apps.news.models import News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "content")

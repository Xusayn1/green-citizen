from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.shared.models import Media


class MyTranslationOption(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'file_type', 'mime_type', 'size', 'created_at')
    list_filter = ('file_type',)
    search_fields = ('original_name', 'mime_type')
    readonly_fields = ('uuid', 'original_name', 'size', 'mime_type', 'file_type', 'created_at', 'updated_at')
    ordering = ('-created_at',)
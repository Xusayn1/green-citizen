from django.contrib import admin

from apps.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'event_date', 'location')
    list_filter = ('event_date',)
    search_fields = ('title', 'description', 'organizer__username')
    ordering = ('event_date',)

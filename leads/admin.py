from django.contrib import admin
from .models import Lead, Visit, Event
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name","email","company","utm_source","created_at")
    search_fields = ("name","email","company")
admin.site.register(Visit)
admin.site.register(Event)

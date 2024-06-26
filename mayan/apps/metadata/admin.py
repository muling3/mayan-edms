from django.contrib import admin

from .models.metadata_type_models import MetadataType


@admin.register(MetadataType)
class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'label', 'default', 'lookup', 'validation', 'parser'
    )

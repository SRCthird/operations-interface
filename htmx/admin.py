from django.contrib import admin
from . import models, forms

# Register your models here.
@admin.register(models.Element)
class ElementAdmin(admin.ModelAdmin):
    form = forms.ElementForm
    list_display = ('id', 'name', 'content')
    list_filter = ('name', 'content',)
    search_fields = ('name', 'content',)

    fieldsets = (
        (None, {
            'fields': ('name', 'content',)
        }),
    )

@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'url')
    list_filter = ('id', 'name', 'url',)
    search_fields = ('id', 'name', 'url',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'photo',)
        }),
    )
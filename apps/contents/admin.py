from django.contrib import admin

from . import models

# Register your models here.
from .crons import generate_static_index_html


@admin.register(models.ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key']
    list_editable = []
    list_per_page = 20
    list_filter = ['key']



    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_index_html()

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_index_html()


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'url', 'image_data', 'status', 'sequence']
    list_editable = ['title', 'url',  'status', 'sequence']
    search_fields = ['title']
    list_filter = ['category','title','status']
    readonly_fields = ('image_data',)

    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_index_html()

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_index_html()

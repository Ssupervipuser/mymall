from django.contrib import admin
from . import models

# Register your models here.
from .crons import generate_static_index_html


@admin.register(models.ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key']
    list_editable = []
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_index_html()

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_index_html()


@admin.register(models.Content)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'url', 'image', 'status', 'text', 'sequence']
    list_editable = ['title', 'url', 'image', 'status', 'text', 'sequence']
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_index_html()

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_index_html()

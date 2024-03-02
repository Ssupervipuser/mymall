from django.contrib import admin
from . import models

# Register your models here.
from .crons import generate_static_index_html


class Admin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()


    def delete_model(self, request, obj):
        obj.delete()



admin.site.register(models.ContentCategory)
admin.site.register(models.Content)

generate_static_index_html()

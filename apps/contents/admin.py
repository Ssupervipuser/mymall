from django.contrib import admin
from . import models

# Register your models here.
from .crons import generate_static_index_html


class Admin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_index_html()



    def delete_model(self, request, obj):
        obj.delete()
        generate_static_index_html()



admin.site.register(models.ContentCategory,Admin)
admin.site.register(models.Content,Admin)



from django.contrib import admin
from . import models
# Register your models here.
from .utils import generate_static_list_search_html

generate_static_list_search_html()
class GoodsCategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_list_search_html()
        print('ok')

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_list_search_html()



admin.site.register(models.GoodsCategory,GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel,GoodsCategoryAdmin)
admin.site.register(models.Goods,GoodsCategoryAdmin)
admin.site.register(models.Brand,GoodsCategoryAdmin)
admin.site.register(models.GoodsSpecification,GoodsCategoryAdmin)
admin.site.register(models.SpecificationOption,GoodsCategoryAdmin)
admin.site.register(models.SKU,GoodsCategoryAdmin)
admin.site.register(models.SKUSpecification,GoodsCategoryAdmin)
admin.site.register(models.SKUImage,GoodsCategoryAdmin)


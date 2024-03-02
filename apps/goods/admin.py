from django.contrib import admin
from . import models
# Register your models here.
from .static_detail import generate_static_sku_detail_html
from .utils import generate_static_list_search_html

generate_static_list_search_html()
class GoodsCategoryAdmin(admin.ModelAdmin):

    """liebiao"""
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_list_search_html()

        print('ok')

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_list_search_html()


class SKUAdmin(admin.ModelAdmin):
    """商品模型站点管理类"""
    def save_model(self, request, obj, form, change):
        obj.save()

        generate_static_sku_detail_html(obj.id)

class SKUImageAdmin(admin.ModelAdmin):
    """商品图片模型站点管理"""
    def save_model(self, request, obj, form, change):
        obj.save()
        sku=obj.sku   #通过外键获取图片模型对象所关联的sku模型的id
        #如果当前sku商品还没有默认图片，就给他设置一张默认图片
        if not sku.default_image_url:
            sku.default_image_url=obj
        generate_static_sku_detail_html(sku.id)

    def delete_model(self, request, obj):
        obj.delete()
        sku=obj.sku     #获取到图片模型对象关联的sku模型
        generate_static_sku_detail_html(sku.id)


admin.site.register(models.GoodsCategory,GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel,GoodsCategoryAdmin)
admin.site.register(models.Goods,GoodsCategoryAdmin)
admin.site.register(models.Brand,GoodsCategoryAdmin)
admin.site.register(models.GoodsSpecification,GoodsCategoryAdmin)
admin.site.register(models.SpecificationOption,GoodsCategoryAdmin)
admin.site.register(models.SKU,SKUAdmin)
admin.site.register(models.SKUSpecification,SKUAdmin)
admin.site.register(models.SKUImage,SKUImageAdmin)


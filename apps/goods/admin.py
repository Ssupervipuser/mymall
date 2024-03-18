from django.contrib import admin
from .models import *
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
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    search_fields = ['id','name']
    list_filter = ['category']
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


admin.site.register(GoodsCategory,GoodsCategoryAdmin)
admin.site.register(GoodsChannel)
admin.site.register(Goods)
admin.site.register(Brand)
admin.site.register(GoodsSpecification)
admin.site.register(SpecificationOption)
admin.site.register(SKU,SKUAdmin)
admin.site.register(SKUSpecification)
admin.site.register(SKUImage,SKUImageAdmin)


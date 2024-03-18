from django.contrib import admin
from .models import *
# Register your models here.
from .static_detail import generate_static_sku_detail_html
from .utils import generate_static_list_search_html

generate_static_list_search_html()
admin.site.site_header = '优选生活管理后台'

admin.site.index_title = '欢迎使用优选生活后台管理'


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_editable = ['parent']
    list_per_page = 10

    """liebiao"""

    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_list_search_html()

        print('ok')

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_list_search_html()


@admin.register(GoodsChannel)
class GoodsChannelAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'url', 'sequence', 'category']
    # list_display_links = ['group_id']
    list_editable = ['category', 'url', 'sequence']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_data', 'first_letter', ]
    # list_editable = ['value']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['brand', 'category1', 'category2', 'category3']
    list_editable = [ 'category1', 'category2', 'category3']
    list_per_page = 10


@admin.register(GoodsSpecification)
class GoodsSpecificationAdmin(admin.ModelAdmin):
    list_display = ['goods', 'name']
    list_editable = ['name']


@admin.register(SpecificationOption)
class SpecificationOptionAdmin(admin.ModelAdmin):
    list_display = ['spec', 'value']
    list_editable = ['value']


############################################
@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    """商品模型站点管理类"""
    # def get_list_display(self, request):
    # list_select_related = ['goods']
    list_display = ['id', 'name', 'goods', 'market_price', 'cost_price', 'price', 'stock', 'sales','is_launched', 'comments',
                    'image_data']
    search_fields = ['id', 'name']
    list_filter = ['category']
    list_editable = ['market_price', 'cost_price', 'price', 'stock','is_launched']
    readonly_fields = ('image_data',)
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.save()

        generate_static_sku_detail_html(obj.id)


@admin.register(SKUImage)
class SKUImageAdmin(admin.ModelAdmin):
    """商品图片模型站点管理"""
    list_display = ['id', 'sku', 'image_data']
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.save()
        sku = obj.sku  # 通过外键获取图片模型对象所关联的sku模型的id
        # 如果当前sku商品还没有默认图片，就给他设置一张默认图片
        if not sku.default_image_url:
            sku.default_image_url = obj
        generate_static_sku_detail_html(sku.id)

    def delete_model(self, request, obj):
        obj.delete()
        sku = obj.sku  # 获取到图片模型对象关联的sku模型
        generate_static_sku_detail_html(sku.id)


@admin.register(SKUSpecification)
class SKUSpecificationAdmin(admin.ModelAdmin):
    list_display = ['sku', 'spec', 'option', ]
    list_editable = ['spec', 'option', ]
    list_per_page = 10

from django.contrib import admin

# Register your models here.
from apps.orders.models import *


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_editable = []


@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    list_editable = []

from rest_framework import serializers

from .models import SKU
# from .search_indexes import SKUIndex
from .search_indexes import SKUIndex


class SKUSerializer(serializers.ModelSerializer):
    """sku商品序列化器"""

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'comments']





from drf_haystack.serializers import HaystackSerializer

class SKUSerializer(serializers.ModelSerializer):
    """
    SKU序列化器
    """
    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')

class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    object = SKUSerializer(read_only=True)

    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'object')
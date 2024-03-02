from rest_framework import serializers

from .models import SKU
# from .search_indexes import SKUIndex


class SKUSerializer(serializers.ModelSerializer):
    """sku商品序列化器"""

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'comments']
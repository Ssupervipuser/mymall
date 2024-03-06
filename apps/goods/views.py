from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .models import SKU
from .serializers import SKUSerializer, SKUIndexSerializer


# # Create your views here.


class SKUListView(ListAPIView):
    """商品列表数据查询"""
    filter_backends = (OrderingFilter,)     #指定后端为排序过滤
    ordering_fields = ('create_time', 'price', 'sales')     #指定排序字段
    serializer_class = SKUSerializer

    def get_queryset(self):
        category_id=self.kwargs.get('category_id')
        return SKU.objects.filter(is_launched=True,category_id=category_id)



from drf_haystack.viewsets import HaystackViewSet

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer
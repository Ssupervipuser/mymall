#地址模块
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from .models import Area
from rest_framework.response import Response
from .serializers import AreaSerializer,SubsSerializer
from rest_framework import status
from rest_framework_extensions.cache.mixins import CacheResponseMixin

# Create your views here.

class ArealistView(APIView):
    """查询所有省"""

    @cache_response(timeout=60*60,cache='default')
    def get(self,request):
        #1.获取指定的查询集
        qs= Area.objects.filter(parent=None)
        #创建序列化器进行序列化
        serializer=AreaSerializer(qs,many=True)

        return Response(serializer.data)

class AreaDetailView(APIView):
    """查询单一省或市"""

    @cache_response(timeout=60 * 60, cache='default')
    def get(self,request,pk):
        #1.根据pk查询出指定的省或市
        try:
            area=Area.objects.get(id=pk)
        except Area.DoesNotExist:
            return Response({'messsage':'无效pk'},status=status.HTTP_400_BAD_REQUEST)
        #创建序列化器进行序列化
        serializer=SubsSerializer(area)

        return Response(serializer.data)
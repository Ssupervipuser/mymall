from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime
from rest_framework_jwt.settings import api_settings

from ..orders.models import OrderInfo

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

from .models import User, Address
from apps.users.serializer import *
from rest_framework.permissions import IsAuthenticated

from django_redis import get_redis_connection
from apps.goods.models import SKU
from ..carts.utils import merge_cart_cookie_to_redis


class CreateUser(CreateAPIView):
    serializer_class = CreateUserSerializer









# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """

    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


class UserDetailView(RetrieveAPIView):
    """"""
    serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    # 重写方法，返回，要展示的用户模型对象
    def get_object(self):
        return self.request.user


####用户收货地址###################################
class AddressViewSet(UpdateModelMixin, GenericViewSet):
    """用户收货地址添加\修改UpdateModelMixin"""


    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

    # queryset = ''
    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)
        # return Address.objects.filter(is_deleted=False)

    def create(self, request):
        user = request.user
        # count = user.addresses.all().count()
        count = Address.objects.filter(user=user).count()
        # 用户收货地址数量有上限  最多只能有20
        if count >= 20:
            return Response({'message': '收货地址数量超过上限'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建序列化器进行反序列化
        serializer = self.get_serializer(data=request.data)
        # 调用序列化器的is_valid()
        serializer.is_valid(raise_exception=True)
        # 调用序列化器的save()
        serializer.save()
        # 响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    ##查询
    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 20,
            'addresses': serializer.data,
        })

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # 修改备注
    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)  # 自定义添加路由
    def title(self, request, pk=None):
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


#################用户浏览记录##############
class UserBrowserHistoryView(CreateAPIView):
    serializer_class = UserBrowserHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self,request):
        """查询浏览记录"""
        #创建redis连接对象
        redis_conn=get_redis_connection('history')
        #获取当前用户
        user=request.user
        #获取reids中当前用户的浏览记录
        sku_ids=redis_conn.lrange('history_%id'%user.id,0,-1)
        #把sku_id的sku模型查询出来
        # SKU.objects.filter(id_in=sku_ids)
        sku_list=[]
        for sku_id in sku_ids:
            sku=SKU.objects.get(id=sku_id)
            sku_list.append(sku)
        #创建序列化器，序列化
        serializer=SKUSerializer(sku_list,many=True)

        return Response(serializer.data)



#继承drf。obt重写登录方法实现购物车合并
class UserAuthorizeView(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)

            #登陆时合并购物车
            merge_cart_cookie_to_redis(request, user, response)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def vision(request):
    user_count = User.objects.count()
    order_count=OrderInfo.objects.count()
    context = {
        'user_count': user_count,
        'order_count': order_count,
    }
    return render(request, '../templates/vision.html', context)
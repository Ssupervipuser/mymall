from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveAPIView
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializer import CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.serializer import UserDetailSerializer



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

    permission_classes = [IsAuthenticated]      #指定权限，只有通过认证的用户才能访问当前视图

    #重写方法，返回，要展示的用户模型对象
    def get_object(self):

        return self.request.user
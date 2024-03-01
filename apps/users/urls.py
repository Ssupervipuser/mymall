from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from apps.users.views import *

urlpatterns = [
    path('users/', CreateUser.as_view()),
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    # path('users/change_password/', CreateUser.as_view()),
    # login
    path('authorizations/', obtain_jwt_token),
    # userdetail
    path('user/', UserDetailView.as_view()),
]

router = routers.DefaultRouter()
router.register('addresses', AddressViewSet, basename='addresses')

urlpatterns += router.urls

# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title

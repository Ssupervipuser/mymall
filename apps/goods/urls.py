from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.goods.views import SKUListView, SKUSearchViewSet

urlpatterns=[
    #商品列表数据
    path('categories/<category_id>/skus/',SKUListView.as_view()),
]


router = DefaultRouter()
router.register('skus/search', SKUSearchViewSet, basename='skus_search')


urlpatterns += router.urls
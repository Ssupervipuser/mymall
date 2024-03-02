from django.urls import path
from apps.goods.views import SKUListView
urlpatterns=[
    #商品列表数据
    path('categories/<category_id>/skus/',SKUListView.as_view()),
]
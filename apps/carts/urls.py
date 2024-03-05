from django.urls import path
from apps.carts.views import *
urlpatterns=[
    #购物车增删改查
    path('carts/',CartView.as_view()),
    path('carts/selection/',CartSelectedAllView.as_view()),
]
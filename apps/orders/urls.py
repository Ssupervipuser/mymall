from django.urls import path
from apps.orders.views import *
urlpatterns=[
    #去结算
    path('orders/settlement/',OrderSettlementView.as_view()),
    #保存订单
    path('orders/',CommitOrderView.as_view())

]
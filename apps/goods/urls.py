from django.urls import path
from apps.goods.views import SKUListView
urlpatterns=[
    path('categories/<category_id>/skus/',SKUListView.as_view()),
]
from django.urls import path

from .views import ArealistView,AreaDetailView

urlpatterns=[
    path('areas/',ArealistView.as_view()),
    path('areas/<pk>/',AreaDetailView.as_view()),
]

from django.urls import path
from .views import *
urlpatterns = [
    path('sms_codes/<mobile:mobile>/', SMSCodeView.as_view()),

]
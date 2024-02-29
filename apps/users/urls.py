from django.urls import path
from apps.users.views import *
urlpatterns = [
    path('users/', CreateUser.as_view()),
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
]
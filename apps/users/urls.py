from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from apps.users.views import *
urlpatterns = [
    path('users/', CreateUser.as_view()),
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    #login
    path('authorizations/',obtain_jwt_token)
]
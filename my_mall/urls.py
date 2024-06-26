"""
URL configuration for my_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

from utils.converters import UsernameConverter, MobileConverter
from django.urls import register_converter

register_converter(UsernameConverter, 'username')
register_converter(MobileConverter, 'mobile')

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('echart/', include('smart_chart.echart.urls')),
    # path('', RedirectView.as_view(url='/echart/index/')),  # 首页,可自定义路由
    path('ckeditor/', include('ckeditor_uploader.urls')),


    path('', include('apps.users.urls')),
    path('', include('apps.verifications.urls')),
    path('', include('apps.areas.urls')),
    path('', include('apps.goods.urls')),
    path('', include('apps.carts.urls')),
    path('', include('apps.orders.urls')),

]

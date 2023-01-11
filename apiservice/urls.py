"""apiservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from apiservice.apps.user.router import router
from apiservice.apps.news.router import routerNows
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apiservice.apps.user.login import Login
from apiservice.apps.user.api import ChangePasswordAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(routerNows.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/news/', include('apiservice.apps.commentary.urls')),
    path('api/authentication/login/', Login.as_view(), name= 'login'),
    path('api/user-change-password/', ChangePasswordAPIView.as_view(), name='change-password' ),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
 
]

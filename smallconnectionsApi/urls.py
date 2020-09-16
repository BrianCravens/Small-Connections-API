"""smallconnectionsApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from connectAPI import models
from connectAPI.views import *
from connectAPI.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'members', Members, 'member')
router.register(r'groups', Groups, 'group')
router.register(r'membergroups', MemberGroups, 'membergroup')
# router.register(r're', MemberGroups, 'membergroup')
# router.register(r'meetings', Meetings, 'meeting')
# router.register(r'messages', Messages, 'message')
# router.register(r'prayers', Prayers, 'prayer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

"""YCBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import welcome
from .views import me
from .views import coding
from .views import reading
from .views import living
from .views import post

urlpatterns = [
    url(r'^god/mode/', include(admin.site.urls)),
    url(r'^$', welcome),
    url(r'^me/?$',me),
    url(r'^coding/?$',coding,name='coding'),
    url(r'^reading/?$',reading),
    url(r'^living/?$',living),
    url(r'^YCNote/post/(?P<pk>\d+)(?:\.json)?',post),

]

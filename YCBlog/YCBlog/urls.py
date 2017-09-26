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
from .views import tag
from .views import post
from .views import login
from .views import logout
from .views import myadmin
from .views import post_edit
from .views import post_delete
from .views import post_preview
from .views import log
from .views import flush_cache
from .views import google_console
# TO-DO: from .views import static_handle

urlpatterns = [
    #url(r'^god/mode/', include(admin.site.urls)),
    url(r'^$', welcome),
    url(r'^me/?$',me),
    url(r'^coding/?$',coding,name='coding'),
    url(r'^reading/?$',reading),
    url(r'^living/?$',living),
    url(r'^tag__(?P<tag>.+)(?:\.json)?',tag),
    url(r'^YCNote/post/(?P<pk>\d+)(?:\.json)?',post),
    url(r'^god/login/$',login),
    url(r'^god/admin/$',myadmin),
    url(r'^god/admin/posts/(?P<pk>\d+)$',post_edit),
    url(r'^god/admin/posts/(?P<pk>\d+)/delete$',post_delete),
    url(r'^god/admin/posts/(?P<pk>\d+)/preview$',post_preview),
    url(r'^god/logout/$',logout),
    url(r'^god/admin/log/$',log),
    url(r'^god/admin/flush_cache/$',flush_cache),
    url(r'^googleb03eb416eb102f2d.html',google_console),
    #url(r'^static/(?P<file>\d+)',static_handle)

]

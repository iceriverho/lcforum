# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import ListView
from django.conf import settings
from django.conf.urls.static import static

from . import models
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^forum/$', ListView.as_view(
        model=models.Post,
        template_name='forum/post/list.html',
        paginate_by=25,
        page_kwarg='p'
    ), name='forum-index'),
    url(r'^forum/thread/(?P<pk>\d+)/$', views.ThreadDetail.as_view(), name='post-detail'),
    url(r'^forum/thread/(?P<pk>\d+)/reply/$', views.ReplyToPost.as_view(), name='post-reply'),
    url(r'^forum/thread/(?P<pk>\d+)/reply/(?P<reply_pk>\d+)/$', views.ReplyToPost.as_view(), name='post-reply-cited'),
    url(r'^forum/node/$', views.ListView.as_view(
        model=models.NodeTag,
        template_name='forum/nodetag/list.html'
    ), name='nodetag-list'),
    url(r'^forum/node/(?P<slug>\w+)/$', views.NodetagDetail.as_view(), name='nodetag-detail'),
    url(r'^forum/node/(?P<slug>\w+)/post/$', views.CreatePost.as_view(), name='nodetag-post'),
    url(r'^auth/reg/$', views.RegView.as_view(), name='user-reg'),
    url(r'^auth/login/$', 'django.contrib.auth.views.login', {
        'template_name': 'forum/auth/login.html'
    }, name='user-login'),
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout_then_login', name='user-logout'),
    url(r'^upload/$', views.UploadView.as_view(), name='upload-view'),
    url(r'^attachment/(?P<pk>\d+)/', views.DetailView.as_view(
        model=models.Attachment,
        template_name='forum/attachment.html'
    ), name='attachment-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
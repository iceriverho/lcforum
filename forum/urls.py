# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import ListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from . import models
from . import views

sitemap_thread_by_admin = {
    'queryset': models.Post.objects.filter(bygod=True),
    'date_field': 'last_edited'
}

sitemap_threads = {
    'queryset': models.Post.objects.filter(bygod=False),
    'date_field': 'last_edited'
}

sitemaps = {
    'thread_by_admin': GenericSitemap(sitemap_thread_by_admin, priority=0.7),
    'threads': GenericSitemap(sitemap_threads, priority=0.5),
}

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
    url(r'^attachments/$', views.ListView.as_view(
        model=models.Attachment,
        template_name='forum/attachments.html',
        paginate_by=15,
        page_kwarg='p'
    ), name='attachment-list'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
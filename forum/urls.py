# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import ListView

from . import models
from . import views


urlpatterns = [
    url(r'^$', ListView.as_view(
        model=models.Post,
        template_name='forum/post/list.html'
    ), name='index'),
    url(r'^forum/$', ListView.as_view(
        model=models.Post,
        template_name='forum/post/list.html'
    ), name='forum-index'),
    url(r'^forum/thread/(?P<pk>\d+)/$', views.DetailView.as_view(
        model=models.Post,
        template_name='forum/post/detail.html'
    ), name='post-detail'),
    url(r'^forum/thread/(?P<pk>\d+)/reply/$', views.ReplyToPost.as_view(), name='post-reply'),
    url(r'^forum/node/$', views.ListView.as_view(
        model=models.NodeTag,
        template_name='forum/nodetag/list.html'
    ), name='nodetag-list'),
    url(r'^forum/node/(?P<pk>\d+)/$', views.DetailView.as_view(
        model=models.NodeTag,
        template_name='forum/nodetag/detail.html'
    ), name='nodetag-detail'),
    url(r'^forum/node/(?P<pk>\d+)/post/$', views.CreatePost.as_view(), name='nodetag-post'),
    url(r'^blog/$', views.BlogList.as_view(), name='blog-list'),
    url(r'^blog/(?P<pk>\d+)/$', views.BlogListByNode.as_view(), name='blog-node'),
    url(r'^blog/article/(?P<pk>\d+)/$', views.DetailView.as_view(
        model=models.Post,
        template_name='forum/blog/detail.html'
    ), name='blog-detail'),
]
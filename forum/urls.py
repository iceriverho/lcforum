# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import (
    UserViewSet, PostViewSet, NodeTagViewSet,
    blog_list, blog_node, blog_detail, index
)
from .routers import LCForumRouter

router = LCForumRouter()
router.register(r'user', UserViewSet)
router.register(r'thread', PostViewSet)
router.register(r'node', NodeTagViewSet)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^forum/', include(router.urls)),
    url(r'^blog/$', blog_list, name='blog-list'),
    url(r'^blog/(?P<pk>\d+)/$', blog_node, name='blog-node'),
    url(r'^blog/article/(?P<pk>\d+)/$', blog_detail, name='blog-detail')
]
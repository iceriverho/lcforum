# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import UserViewSet, PostViewSet, NodeTagViewSet, blog_view
from .routers import LCForumRouter

router = LCForumRouter()
router.register(r'user', UserViewSet)
router.register(r'thread', PostViewSet)
router.register(r'node', NodeTagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'blog/', blog_view)
]
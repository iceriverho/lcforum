# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostViewSet, NodeTagViewSet
from .routers import LCForumRouter

router = LCForumRouter()
router.register(r'user', UserViewSet)
router.register(r'thread', PostViewSet)
router.register(r'node', NodeTagViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
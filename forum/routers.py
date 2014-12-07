# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter
from .views import PostViewSet

class LCForumRouter(DefaultRouter):
    def get_api_root_view(self):
        return PostViewSet.as_view({'get': 'list'})
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .models import Post, NodeTag
from .serializers import UserSerializer, PostSerializer, NodeTagSerializer
from .permissions import IsOwnerOrReadOnly, AllowNewuser
from .mixins import TemplatesMixin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowNewuser, )


class PostViewSet(viewsets.ModelViewSet, TemplatesMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if isinstance(self.request.user, User) else None)


class NodeTagViewSet(viewsets.ModelViewSet):
    queryset = NodeTag.objects.all()
    serializer_class = NodeTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
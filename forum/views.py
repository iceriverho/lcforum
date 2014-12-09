from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Post, NodeTag, Reply
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

    @detail_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def reply(self, request, pk=None):
        post_node = self.get_object()
        reply = Reply(
            author=request.user if request.user.is_authenticated() else None,
            post_node=post_node,
            title=request.data['title'],
            content=request.data['content']
        )
        try:
            reply.save()
            return Response({'status': 'Successfully replied.'})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated() else None)


class NodeTagViewSet(viewsets.ModelViewSet):
    queryset = NodeTag.objects.all()
    serializer_class = NodeTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    @detail_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def post(self, request, pk=None):
        node = self.get_object()
        thread = Post(
            author=request.user if request.user.is_authenticated() else None,
            node=node,
            title=request.data['title'],
            content=request.data['content']
        )
        try:
            thread.save()
            return Response({'status': 'Successfully posted.'})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
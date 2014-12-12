from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Post, NodeTag, Reply
from .serializers import UserSerializer, PostSerializer, NodeTagSerializer
from .permissions import IsOwnerOrReadOnly, AllowNewuser
from .mixins import TemplatesMixin
from .forms import ReplyForm, ThreadForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowNewuser, )


class PostViewSet(viewsets.ModelViewSet, TemplatesMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @detail_route(methods=['get', 'post'], permission_classes=[permissions.AllowAny])
    def reply(self, request, pk=None):
        post_node = self.get_object()

        if request.method == 'GET':
            return render_to_response(
                'forum/reply.html',
                {'form': ReplyForm(
                    initial={'title': 'Re:' + post_node.title}
                ), 'post_node': post_node},
                context_instance=RequestContext(request)
            )

        reply = Reply(
            author=request.user if request.user.is_authenticated() else None,
            post_node=post_node,
            title=request.data['title'] if request.data['title'] != '' else "Re:" + request.data['title'],
            content=request.data['content'],
            bygod=request.data.get('bygod', False)
        )
        try:
            reply.save()
            return redirect('post-detail', pk=post_node.pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated() else None)


class NodeTagViewSet(viewsets.ModelViewSet, TemplatesMixin):
    queryset = NodeTag.objects.all()
    serializer_class = NodeTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def list(self, request, *args, **kwargs):
        return render_to_response(
            'forum/nodetag/list.html',
            {'context_data': self.get_queryset()},
            context_instance=RequestContext(request)
        )

    @detail_route(methods=['get', 'post'], permission_classes=[permissions.AllowAny])
    def post(self, request, pk=None):
        node = self.get_object()

        if request.method == 'GET':
            return render_to_response(
                'forum/post.html',
                {'form': ThreadForm(), 'node': node},
                context_instance=RequestContext(request)
            )

        thread = Post(
            author=request.user if request.user.is_authenticated() else None,
            node=node,
            title=request.data['title'],
            content=request.data['content'],
            bygod=request.data.get('bygod', False)
        )
        try:
            thread.save()
            return redirect('nodetag-detail', pk=node.pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def blog_list(request):
    posts = Post.objects.filter(bygod=True)
    replies = Reply.objects.filter(bygod=True)
    return render_to_response(
        'forum/blog/list.html',
        {'posts': posts, 'replies': replies},
        context_instance=RequestContext(request)
    )


def blog_node(request, pk=None):
    node = get_object_or_404(NodeTag, pk=pk)
    posts = Post.objects.filter(bygod=True, node=node)
    return render_to_response(
        'forum/blog/node.html',
        {'posts': posts, 'node': node},
        context_instance=RequestContext(request)
    )


def blog_detail(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    return render_to_response(
        'forum/blog/detail.html',
        {'post': post},
        context_instance=RequestContext(request)
    )

def index(request):
    return redirect('api-root')
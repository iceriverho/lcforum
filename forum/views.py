# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.models import modelform_factory
from django.forms.widgets import PasswordInput

from .models import Post, NodeTag, Reply
from .forms import ReplyForm


class IndexView(ListView):
    model = Post
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        return {'post_latest': self.get_queryset().filter(bygod=False).order_by('-created'),
                'blog_latest': self.get_queryset().filter(bygod=True).order_by('-created')}


class NodetagDetail(ListView):
    model = Post
    template_name = 'forum/nodetag/detail.html'
    paginate_by = 25
    page_kwarg = 'p'

    def get_queryset(self):
        all_posts = super(NodetagDetail, self).get_queryset()
        posts_belong_to_this_node = all_posts.filter(node=self.kwargs['pk'])
        return posts_belong_to_this_node

    def get_context_data(self, **kwargs):
        context = super(NodetagDetail, self).get_context_data(**kwargs)
        context['nodetag'] = get_object_or_404(NodeTag, pk=self.kwargs['pk'])
        return context


class BlogList(ListView):
    queryset = Post.objects.filter(bygod=True).order_by('node', '-created')
    template_name = 'forum/blog/list.html'

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['reply_list'] = Reply.objects.filter(bygod=True)
        return context


class BlogListByNode(DetailView):
    model = NodeTag
    template_name = 'forum/blog/node.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListByNode, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(bygod=True, node=self.object)
        return context


class ReplyToPost(CreateView):
    form_class = ReplyForm
    template_name = 'forum/reply.html'
    post_node = None

    def form_valid(self, form):
        form.instance.author = self.request.user if self.request.user.is_authenticated() else None
        form.instance.post_node = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super(ReplyToPost, self).form_valid(form)

    def get_initial(self):
        self.post_node = get_object_or_404(Post, pk=self.kwargs['pk'])
        return {'title': 'Re:' + self.post_node.title}

    def get_context_data(self, **kwargs):
        context = super(ReplyToPost, self).get_context_data(**kwargs)
        context['post_node'] = self.post_node
        return context


class CreatePost(CreateView):
    model = Post
    fields = ['title', 'content', 'bygod']
    template_name = 'forum/post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user if self.request.user.is_authenticated() else None
        form.instance.node = get_object_or_404(NodeTag, pk=self.kwargs['pk'])
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['node'] = get_object_or_404(NodeTag, pk=self.kwargs['pk'])
        return context


class RegView(FormView):
    template_name = 'forum/auth/reg.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        username = request.POST['username']
        email = request.POST.get('email', None)
        password = request.POST['password']

        if form.is_valid():
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.object = authenticate(
                username=username,
                password=password
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        # See this: http://stackoverflow.com/a/9899170
        return self.kwargs.get('next', '/')

    def form_valid(self, form):
        # See this: http://stackoverflow.com/a/6039782
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        return modelform_factory(
            User,
            fields=['username', 'email', 'password'],
            widgets={
                'password': PasswordInput()
            },
            labels={
                'email': u"电子邮箱"
            }
        )
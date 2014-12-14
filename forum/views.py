from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView

from .models import Post, NodeTag, Reply


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
    model = Reply
    fields = ['title', 'content', 'bygod']
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
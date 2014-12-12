# -*- coding: utf-8 -*-

from django.forms import ModelForm
from .models import Reply, Post

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['title', 'content', 'bygod']

class ThreadForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'bygod']

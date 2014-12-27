# -*- coding: utf-8 -*-

from django.forms import ModelForm
from .models import Reply

class ReplyForm(ModelForm):
    error_css_class = 'error-item'

    class Meta:
        model = Reply
        fields = ['title', 'content', 'bygod']
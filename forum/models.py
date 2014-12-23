# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
import markdown

# 一般来说，默认只有主键被索引了（db_index = True）
# 增加索引一般只有对数据比较多的时候才有意义，而且增加了主键后每次增删改都会重建索引
class DateTimeBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostBase(DateTimeBase):
    title = models.CharField(max_length=200, error_messages={
        'blank': u"标题不能为空",
        'null': u"标题不能为空",
        'invalid': u"您输入了一个无效的标题，标题的长度请控制在100个字符内"
    }, help_text=u"☞标题为必填且不能超过100个字符",
                             verbose_name=u"标题")
    content = models.TextField(blank=True, null=True,
                               help_text=u"☞正文可以留空，但不要输入无意义的内容",
                               verbose_name=u"正文")
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s', on_delete=models.SET_NULL)
    content_md = models.TextField(blank=True, null=True)
    bygod = models.BooleanField(blank=True, default=False,
                                help_text=u"☞将这篇文章归入管理员文集",
                                verbose_name=u"归档")

    def save(self, *args, **kwargs):
        self.bygod = self.bygod if getattr(self.author, 'is_superuser', False) else False
        self.content_md = markdown.markdown(self.content, safe_mode='escape')
        super(PostBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class NodeTag(DateTimeBase):
    name = models.CharField(max_length=50, error_messages={
        'blank': u"节点的名称不能为空",
        'null': u"节点的名称不能为空",
        'invalid': u"您输入了一个无效的节点名称，节点名称的长度不能超过50个字符"
    }, help_text=u"☞节点名称为必填且不能超过50个字符",
                            verbose_name=u"节点名称")
    description = models.TextField(blank=True, null=True,
                                   help_text=u"☞关于节点讨论主题的简要描述",
                                   verbose_name=u"节点描述")

    def get_absolute_url(self):
        return reverse('nodetag-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name


class Post(PostBase):
    node = models.ForeignKey(NodeTag, null=True, related_name='posts', on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title


class Reply(PostBase):
    post_node = models.ForeignKey(Post, null=True, related_name='replies', on_delete=models.SET_NULL)

    def get_absolute_url(self):
        if getattr(self.post_node, 'pk', None):
            return reverse('post-detail', kwargs={'pk': self.post_node.pk})

        return reverse('forum-index')

    def __unicode__(self):
        return "#{0} reply of '{1}'".format(self.pk, self.post_node.title)

    class Meta:
        verbose_name_plural = 'replies'
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.core import validators
import markdown
from .utility import get_file_path
from PIL import Image
import os.path


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
    }, help_text=u"☞标题为必填且不能超过100个字符", verbose_name=u"标题")
    content = models.TextField(blank=True, null=True,
                               help_text=u"☞内容可以留空，但不要输入无意义的内容",
                               verbose_name=u"内容")
    author = models.ForeignKey(User, blank=True, null=True, related_name='%(class)s', on_delete=models.SET_NULL)
    content_md = models.TextField(blank=True, null=True)
    bygod = models.BooleanField(blank=True, default=False,
                                help_text=u"☞将这篇文章归入管理员文集",
                                verbose_name=u"归档")
    guest_name = models.CharField(max_length=30, default="Guest", verbose_name=u"游客称呼", blank=True, null=True,
                                  validators=[
                                      validators.RegexValidator(r'^[\w.@+-]+$', u"名字中包含不允许的字符.", 'invalid')
                                  ])
    guest_email = models.EmailField(
        max_length=254, verbose_name=u"游客联系方式", blank=True, null=True,
        help_text=u"您的邮件地址在显示时会将@替换为[at]",
        error_messages={
            'invalid': u"您输入了一个无效的邮件地址，请修改或留空"
        }
    )
    ip_addr = models.IPAddressField(default='0.0.0.0', verbose_name=u"IP地址", help_text=u"发信人的IP地址")

    def save(self, *args, **kwargs):
        self.bygod = self.bygod if getattr(self.author, 'is_superuser', False) else False
        self.content_md = markdown.markdown(
            self.content,
            safe_mode='escape',
            output_format='html5',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.sane_lists',
                'markdown.extensions.codehilite(noclasses=True, linenums=False)',
                'markdown.extensions.toc'
            ]
        )
        super(PostBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class NodeTag(DateTimeBase):
    name = models.CharField(max_length=50, error_messages={
        'blank': u"节点的名称不能为空",
        'null': u"节点的名称不能为空",
        'invalid': u"您输入了一个无效的节点名称，节点名称的长度不能超过50个字符"
    }, help_text=u"☞节点名称为必填且不能超过50个字符", verbose_name=u"节点名称", unique=True)
    description = models.TextField(blank=True, null=True,
                                   help_text=u"☞关于节点讨论主题的简要描述",
                                   verbose_name=u"节点描述")
    slug = models.CharField(max_length=30, help_text=u"☞节点的英文简写", verbose_name=u"节点代号", unique=True)

    def get_absolute_url(self):
        return reverse('nodetag-detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


class Post(PostBase):
    node = models.ForeignKey(NodeTag, null=True, related_name='posts', on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pk']


class Reply(PostBase):
    post_node = models.ForeignKey(Post, null=True, related_name='replies', on_delete=models.SET_NULL)

    def get_absolute_url(self):
        if getattr(self.post_node, 'pk', None):
            return reverse('post-detail', kwargs={'pk': self.post_node.pk})

        return reverse('forum-index')

    def __unicode__(self):
        return u"#{0} reply of '{1}'".format(self.pk, getattr(self.post_node, 'title', 'A Deleted Post'))

    class Meta:
        verbose_name_plural = 'replies'
        ordering = ['-pk']


class Attachment(DateTimeBase):
    width = models.PositiveIntegerField(u"图片宽度", blank=True, null=True, default=0,
                                        help_text=u"图片的宽度，单位为像素(px)")
    height = models.PositiveIntegerField(u"图片长度", blank=True, null=True, default=0,
                                         help_text=u"图片的长度，单位为像素(px)")
    image_format = models.CharField(u"图片格式", max_length=100, blank=True, null=True,
                                    help_text=u"图片的格式")
    is_image = models.BooleanField(u"是否图片文件", blank=True, default=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    remark = models.CharField(u"文件备注", max_length=200, blank=True, null=True,
                              help_text=u"文件上传后会被统一命名，建议加上备注以便查找")
    attachment = models.FileField(u'选择文件', null=True, upload_to=get_file_path,
                                  help_text=u"选择要上传的文件，请不要上传非法、危险以及涉及版权问题的文件")

    def filename(self):
        return os.path.basename(self.attachment.name)

    def file_exists(self):
        return self.attachment and os.path.isfile(self.attachment.path)

    def save(self, *args, **kwargs):
        try:
            pic = Image.open(self.attachment.path.encode('utf-8'))
            self.is_image = True
            self.image_format = pic.format
            self.width, self.height = pic.size
            pic.close()
        except IOError:
            self.is_image = False
            self.width, self.height = 0, 0
        super(Attachment, self).save(*args, **kwargs)
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Reply, Post, NodeTag
from .relations import LinkWithNameRelatedField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    date_joined = serializers.DateTimeField(format=None, read_only=True)
    def create(self, validated_attrs):
        return User.objects.create_user(**validated_attrs)

    def update(self, instance, validated_attrs):
        instance.set_password(validated_attrs.pop('password', instance.password))
        return super(UserSerializer, self).update(instance, validated_attrs)

    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'email', 'date_joined', 'url')
        extra_kwargs = {'password': {'write_only': True}}


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    created = serializers.DateTimeField(format=None, read_only=True)
    last_edited = serializers.DateTimeField(format=None, read_only=True)

    class Meta:
        model = Reply
        fields = ('pk', 'author', 'title', 'content', 'content_md', 'created', 'last_edited')
        read_only_fields = ('created', 'last_edited')
        depth = 1


class PostSerializer(serializers.HyperlinkedModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    # node = serializers.PrimaryKeyRelatedField(queryset=NodeTag.objects.all())
    node = LinkWithNameRelatedField(queryset=NodeTag.objects.all(), view_name='nodetag-detail', slug='name')
    created = serializers.DateTimeField(format=None, read_only=True)
    last_edited = serializers.DateTimeField(format=None, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'author', 'node', 'title', 'content', 'content_md', 'created', 'last_edited', 'replies', 'url')
        depth = 1


class NodeTagSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = NodeTag
        fields = ('pk', 'name', 'description', 'posts', 'url')
        depth = 1
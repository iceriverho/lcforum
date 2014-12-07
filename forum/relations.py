# -*- coding: utf-8 -*-

from rest_framework import serializers

class LinkWithNameRelatedField(serializers.HyperlinkedRelatedField):
    def __init__(self, **kwargs):
        self.slug_field = kwargs.pop('slug', None)
        super(LinkWithNameRelatedField, self).__init__(**kwargs)

    def to_representation(self, value):
        slug = getattr(value, self.slug_field)
        return {'slug': slug, 'url': super(LinkWithNameRelatedField, self).to_representation(value)}
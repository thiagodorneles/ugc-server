# coding: utf-8
from rest_framework import serializers
from ugc.core.models import Publish, Tag

class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = ('title', 'description', 'created_at', 'location', 'city', 'status')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'created_at', 'status')
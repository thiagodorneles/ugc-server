# coding: utf-8
from rest_framework import serializers
from ugc.core.models import Publish, Tag

class PublishSerializer(serializers.ModelSerializer):
    tags = serializers.RelatedField(many=True)
    class Meta:
        model = Publish
    	resource_name = 'publishs'
        fields = ('title', 'description', 'created_at', 'location', 'city', 'status', 'tags')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'created_at', 'status')

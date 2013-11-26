# coding: utf-8
from rest_framework import serializers
from ugc.core.models import Publish, Tag, User

class PublishSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='tag')
    user = serializers.SlugRelatedField(slug_field='id')
    user_name = serializers.Field(source = 'user_name')
    
    class Meta:
        model = Publish
    	resource_name = 'publishs'
        fields = ('title', 'description', 'created_at', 'location', 'city', 'status', 'tags', 
                  'user', 'user_name', 'quant_views', 'quant_blocks', )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'created_at', 'status')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'created_at')
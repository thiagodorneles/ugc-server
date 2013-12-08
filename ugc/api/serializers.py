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
        fields = ('id', 'title', 'description', 'created_at', 'location', 'city', 'status', 'tags', 
                  'user', 'user_name', 'quant_views', 'quant_blocks', )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'created_at', 'status')

class PublishUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = ('id', 'title', 'quant_views', 'quant_blocks')

class UserSerializer(serializers.ModelSerializer):
    results = PublishSerializer(many=True, source='publish_set', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at', 'image_url', 
                  'twitter_user', 'twitter_id', 'twitter_token', 
                  'facebook_user', 'facebook_id', 'facebook_token',
                  'results')

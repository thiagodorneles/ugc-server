# coding: utf-8
from rest_framework import serializers
from ugc.core.models import Publish, Tag, User, Media

class PublishSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='tag')
    user = serializers.SlugRelatedField(slug_field='id')
    user_name = serializers.Field(source = 'user_name')
    images = serializers.RelatedField(many=True, source='media_set')
    thumbs = serializers.Field(source='thumbs')
    
    class Meta:
        model = Publish
    	resource_name = 'publishs'
        fields = ('id', 'title', 'description', 'created_at', 'location', 'city', 'status', 'tags', 
                  'user', 'user_name', 'quant_views', 'quant_blocks', 'images', 'thumbs', )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', 'created_at', 'status')

class PublishUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = ('id', 'title', 'quant_views', 'quant_blocks')

class UserSerializer(serializers.ModelSerializer):
    publishs = PublishSerializer(many=True, source='publish_set', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at', 'image_url', 
                  'twitter_user', 'twitter_id', 'twitter_token', 
                  'facebook_user', 'facebook_id', 'facebook_token',
                  'publishs')

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('image', 'thumbnail', )
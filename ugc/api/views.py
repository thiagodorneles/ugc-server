# coding: utf-8
from ugc.core.models import Publish, Tag
from ugc.api.serializers import PublishSerializer, TagSerializer
from rest_framework import viewsets, mixins

class PublishViewSet(mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Publish.objects.all().filter(status=True)
    serializer_class = PublishSerializer


class TagViewSet(mixins.CreateModelMixin, 
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all().filter(status=True)
    serializer_class = TagSerializer
    search_fields = ('tag')

# coding: utf-8
from ugc.core.models import Publish, Tag, User
from ugc.api.serializers import PublishSerializer, TagSerializer, UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class PublishViewSet(mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    base_name = 'publishs-list'
    queryset = Publish.objects.all().filter(status=True)
    serializer_class = PublishSerializer

class TagViewSet(mixins.CreateModelMixin, 
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all().filter(status=True)
    serializer_class = TagSerializer
    search_fields = ('tag')

class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'publishs': reverse('publishs-list', request=request, format=format),
#         # 'tags': reverse('tag-list', request=request, format=format),
#         # 'users': reverse('user-list', request=request, format=format)
#     })
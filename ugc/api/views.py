# coding: utf-8
from ugc.core.models import Publish, Tag, User
from ugc.api.serializers import PublishSerializer, TagSerializer, UserSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from datetime import datetime
from geopy.geocoders import GoogleV3

class PublishViewSet(mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    base_name = 'publishs-list'
    queryset = Publish.objects.all().filter(status=True)
    serializer_class = PublishSerializer

    def create(self, request, *args, **kwargs):
        tags = request.DATA.get('tags')

        if tags:
            for t in tags:
                Tag.objects.get_or_create(tag=t)
        
        serializer = self.get_serializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if (obj.location):
            geolocator = GoogleV3()
            address, (latitude, longitude) = geolocator.reverse(obj.location)[0]
            obj.city = address.split(',')[2].split('-')[0].strip()

        self.pre_save(serializer.object)
        self.object = serializer.save(force_insert=True)
        self.post_save(self.object, created=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
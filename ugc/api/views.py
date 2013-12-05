# coding: utf-8
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from datetime import datetime
from geopy.geocoders import GoogleV3
from ugc.core.models import Publish, Tag, User
from ugc.api.serializers import PublishSerializer, TagSerializer, UserSerializer

class PublishViewSet(mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    base_name = 'publishs-list'
    queryset = Publish.objects.all().filter(status=True)
    serializer_class = PublishSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Feito ovewrite no metodo retrieve que pertence ao RetrieveModelMixin
        para quando buscar um Publish especifico atualizar a propriedade quant_views
        """
        self.object = self.get_object()
        self.object.update_views()
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        """
        Ovewrite no metodo create que pertence ao CreateModelMixin
        para antes de criar uma nova Publish percorrer todas as tags
        recebidas e criar as que nao existam.
        """
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

# @csrf_exempt
@api_view(['POST'])
def publish_block(request):
    print '================ AQUI ==================\n'
    pk = request.DATA.get('id')

    try:
        publish = Publish.objects.get(pk=pk)
    except Publish.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PublishSerializer(publish, data=request.DATA)
    serializer.object.update_block()
    return Response(serializer.data)

# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'publishs': reverse('publishs-list', request=request, format=format),
#         # 'tags': reverse('tag-list', request=request, format=format),
#         # 'users': reverse('user-list', request=request, format=format)
#     })
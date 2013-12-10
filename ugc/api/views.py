# coding: utf-8
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser
from datetime import datetime
from geopy.geocoders import GoogleV3
from ugc.core.models import Publish, Tag, User, Media
from ugc.api.serializers import PublishSerializer, TagSerializer, UserSerializer, MediaSerializer
from django.db.models import Q

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
            import unicodedata
            for t in tags:
                t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore')
                Tag.objects.get_or_create(tag=t)
        
        serializer = self.get_serializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if (serializer.object.location):
            geolocator = GoogleV3()
            address, (latitude, longitude) = geolocator.reverse(serializer.object.location)[0]
            serializer.object.city = address.split(',')[2].split('-')[0].strip()

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

    def create(self, request, *args, **kwargs):
        """
        Ovewrite no metodo create que pertence ao CreateModelMixin
        para verificar se ja existe algum usuario com o twitter_id ou facebook_id
        """

        twitter_id  = request.DATA.get('twitter_id')
        facebook_id = request.DATA.get('facebook_id')

        try:
            user = User.objects.get(Q(twitter_id=str(twitter_id)) | Q(facebook_id=str(facebook_id)))
        
            if user.twitter_id and not user.facebook_id and facebook_id:
                user.facebook_id    = request.DATA.get('facebook_id')
                user.facebook_token = request.DATA.get('facebook_token')
                user.facebook_user  = request.DATA.get('facebook_user')
            elif user.facebook_id and not user.twitter_id and twitter_id:
                user.twitter_id    = request.DATA.get('twitter_id')
                user.twitter_token = request.DATA.get('twitter_token')
                user.twitter_user  = request.DATA.get('twitter_user')
            # 
            if user.twitter_id:
                user.twitter_user  = request.DATA.get('twitter_user')
                user.twitter_token = request.DATA.get('twitter_token')
                user.image_url     = request.DATA.get('image_url')

            user.save()
            serializer = UserSerializer(user)
        except User.DoesNotExist:

            serializer = self.get_serializer(data=request.DATA)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# @csrf_exempt
@api_view(['POST'])
def publish_block(request):
    pk = request.DATA.get('id')

    try:
        publish = Publish.objects.get(pk=pk)
    except Publish.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PublishSerializer(publish, data=request.DATA)
    serializer.object.update_block()
    return Response(serializer.data)

# class PublishUploadViewSet(mixins.CreateModelMixin, 
#                            mixins.ListModelMixin,
#                            mixins.RetrieveModelMixin,
#                            viewsets.GenericViewSet):
#     serializer_class = MediaSerializer
#     parser_class = (FileUploadParser,)



@api_view(['POST'])
def publish_image(request):
    publish_id = request.DATA.get('publish_id')

    for filename, file in request.FILES.iteritems():
        name = request.FILES[filename].name
        media = Media(image=file, publish_id=publish_id)
        media.save()

    return Response(status=201)

# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'publishs': reverse('publishs-list', request=request, format=format),
#         # 'tags': reverse('tag-list', request=request, format=format),
#         # 'users': reverse('user-list', request=request, format=format)
#     })

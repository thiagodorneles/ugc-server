# coding: utf-8
from django.conf.urls import patterns, include, url
from ugc.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/publishs', views.PublishViewSet)
router.register(r'api/tags', views.TagViewSet)
router.register(r'api/users', views.UserViewSet)
# router.register(r'api/upload', views.PublishUploadViewSet)

urlpatterns = patterns('',
    url(r'^api/block/', 'ugc.api.views.publish_block', name='publish_block'),
    url(r'^api/upload/', 'ugc.api.views.publish_image', name='publish_image'),
    url(r'^api/$', 'ugc.api.views.api_root'),
    url(r'^', include(router.urls)),
)
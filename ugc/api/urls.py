# coding: utf-8
from django.conf.urls import patterns, include, url
from ugc.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/publishs', views.PublishViewSet)
router.register(r'api/tags', views.TagViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
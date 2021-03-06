# coding: utf-8
from django.conf.urls import patterns, include, url
# from ugc.core.views import PublishDetailView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('ugc.core.views',
    url(r'^$', 'homepage', name='homepage'),
    url(r'^sobre/$', 'about', name='about'),
    url(r'^contato/$', 'contact', name='contact'),
    url(r'^publicacao/(\d+)/$', 'detail', name='detail'),
    # url(r'^publicacao/(?P<pk>\d+)/$', PublishDetailView.as_view(), name='detail'),
    # url(r'^pesquisa/(?P<slug>[\d\w]+)/$', 'search', name='search'),
    url(r'^pesquisa/$', 'search', name='search'),
    url(r'^tags/(?P<slug>[\d\w]+)/$', 'search_tags', name='search_tags'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
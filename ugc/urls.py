from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('ugc.core.urls', namespace='core')),
    url(r'', include('ugc.api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)

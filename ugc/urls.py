from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('ugc.core.views',
    url(r'^$', 'homepage', name='homepage'),
    url(r'^publicacao/(\d+)/$', 'detail', name='detail'),
    url(r'^contato/$', 'contact', name='contact'),
    url(r'^sobre/$', 'about', name='about'),
    # Examples:
    # url(r'^$', 'ugc.views.home', name='home'),
    # url(r'^ugc/', include('ugc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('spidergraphs.views',
    url(r'^$','index'),
    url(r'^(?P<institution>[a-z_]+)$','institution'),
    url(r'^(?P<institution>[a-z_]+)/(?P<program_id>[\d]+)$','program'),
    url(r'^(?P<institution>[a-z_]+)/(?P<program_id>[\d]+)/(?P<course_id>[\d]+)$','course'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

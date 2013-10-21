from django.conf.urls import patterns, include, url
from MessageCollector.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^messenger/$',messenger),
    url(r'^sources/$', sourceList),
    url(r'^users/$', userList),
    url(r'^companions/$', companionList),
    url(r'^messages/$', messageList),
    url(r'^test/$', test),

    # Examples:
    # url(r'^$', 'SaimaTelecom.views.home', name='home'),
    # url(r'^SaimaTelecom/', include('SaimaTelecom.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),



    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

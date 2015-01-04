from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web.controllers.index import index


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index),

    url(r'^admin/', include(admin.site.urls)),
    #patterns('django.contrib.staticfiles.views', url(r'^s/(?P<path>.*)$', 'serve'),)
)
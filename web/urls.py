from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web.controllers.index import index
from web.controllers import auth
from web.controllers import avto_fetch


urlpatterns = patterns(''
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    , url(r'^admin/', include(admin.site.urls))
    , url(r'^$', index)
    , url(r'^auth/login', auth.login)
    , url(r'^auth/logout', auth.logout)

    , url(r'^fetch-avto$', avto_fetch.index)
)
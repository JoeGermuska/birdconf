from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
    url(r'^show/(\d{4}-\d{2}-\d{2})$', 'playlists.views.show', name='show'),
    url(r'^track/(?P<slug>[\-\w]+)?$', 'playlists.views.track', name='track'),
    (r'^$', 'playlists.views.last_year'),
    (r'^mardi[-\s]?gras$', 'playlists.views.mardigras'),
    (r'^all/?$', 'playlists.views.all'),
)
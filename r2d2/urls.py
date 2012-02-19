from django.conf.urls.defaults import *

import views

urlpatterns = patterns(
    '',

    url(r'^$',
        'r2d2.views.browse'),

    url(r'^graph/(?P<label>[^/]+)/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/(?P<endtime>\d+)/(?P<showtime>\d+)$',
        'r2d2.views.graph',
        name='graph'),

    url(r'^browse/(?P<host>[^/]+)/$',
        'r2d2.views.browse',
        name='host'),

    url(r'^browse/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/$',
        'r2d2.views.browse',
        name='plugininstance'),

    url(r'^add/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/$',
        'r2d2.views.add_to_dashboard',
        name='add'),

    url(r'^remove/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/$',
        'r2d2.views.remove_from_dashboard',
        name='remove'),

    url(r'^dashboard/$',
	'r2d2.views.dashboard',
        name='dashboard'),

)


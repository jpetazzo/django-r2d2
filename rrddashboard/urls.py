from django.conf.urls.defaults import *

import views

urlpatterns = patterns(
    '',

    url(r'^$',
        'rrddashboard.views.browse'),

    url(r'^graph/(?P<label>[^/]+)/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/(?P<endtime>\d+)/(?P<showtime>\d+)$',
        'rrddashboard.views.graph',
        name='graph'),

    url(r'^browse/(?P<host>[^/]+)/$',
        'rrddashboard.views.browse',
        name='host'),

    url(r'^browse/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/$',
        'rrddashboard.views.browse',
        name='plugininstance'),

    url(r'^add/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/$',
        'rrddashboard.views.add_to_dashboard',
        name='add'),

    url(r'^remove/(?P<host>[^/]+)/(?P<plugininstance>[^/]+)/(?P<rrdfile>[^/]+)/(?P<datasource>[^/]+)/$',
        'rrddashboard.views.remove_from_dashboard',
        name='remove'),

    url(r'^dashboard/$',
	'rrddashboard.views.dashboard',
        name='dashboard'),

)


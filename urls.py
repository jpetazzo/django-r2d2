from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to

import rrddashboard.urls

admin.autodiscover()

urlpatterns = patterns(
    '',

    #(r'^$',
    # redirect_to, dict(url='/rrddashboard/')),

    #(r'^rrddashboard/',
	  #include(rrddashboard.urls)),

    (r'^',
	  include(rrddashboard.urls)),

    (r'^admin/', include(admin.site.urls)),
)


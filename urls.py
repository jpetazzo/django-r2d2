from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to

import r2d2.urls

admin.autodiscover()

urlpatterns = patterns(
    '',

    #(r'^$',
    # redirect_to, dict(url='/r2d2/')),

    #(r'^r2d2/',
	  #include(r2d2.urls)),

    (r'^',
	  include(r2d2.urls)),

    (r'^admin/', include(admin.site.urls)),
)


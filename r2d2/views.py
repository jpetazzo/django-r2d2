from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

import commands
import glob
import os
import re
import rrdtool
import time

from models import Dashboard

RRDPATH = '/var/lib/collectd/rrd'


def get_rrd_plugininstances_for_host(host):
    hostdir = os.path.join(RRDPATH, host)
    if os.path.isdir(hostdir):
        plugininstance_list = os.listdir(hostdir)
        plugininstance_list.append('cpu-*')
        plugininstance_list.sort()
    else:
        plugininstance_list = []
    return plugininstance_list


def graph(request, label, host, plugininstance, rrdfile, datasource,
          endtime=0, showtime=86400, debug=False):
    if rrdfile == 'memory-ram_limit':
        return memorygraph(request, label, host, plugininstance,
                           endtime, showtime)
    rrdfiles = glob.glob('%s/%s/%s/%s.rrd'%(
        RRDPATH, host, plugininstance, rrdfile))
    options = [
        '-', '--imgformat', 'PNG', '--height', '100',
        '--start', 'end-%ss'%showtime, '--end', 'now-%ss'%endtime,
        ]
    i=0
    rpn='CDEF:total=0'
    for rrdfile in rrdfiles:
        options.append('DEF:i%d=%s:%s:AVERAGE'%(i,rrdfile,datasource))
        options.append('LINE:i%d#cccccc:'%i)
        rpn+=',i%d,+'%i
        i+=1
    options.append(rpn)
    options.append('LINE:total#000000:%s'%label)
    options =  " ".join(map(str,options))
    if debug:
        return HttpResponse(options)
    data_image = commands.getoutput("rrdtool graph " + options)
    return HttpResponse(data_image, mimetype="image/png")


def browse(request, host = None, plugininstance = None):
    hosts = sorted(os.listdir(RRDPATH))
    if host != None :
        plugininstances = get_rrd_plugininstances_for_host(host)
        if plugininstance != None :
            all_ds_list = []
            realplugininstance = plugininstance.replace('*','0')
            if os.path.isdir('%s/%s/%s'%(RRDPATH,host,realplugininstance)):
                rrdfiles = os.listdir('%s/%s/%s/' %(
                    RRDPATH, host, realplugininstance))
                for rrdfile in rrdfiles:
                    if not rrdfile.endswith('.rrd'):
                        continue
                    rrdname = rrdfile[:-4]
                    rrdpath = '%s/%s/%s/%s' %(
                        RRDPATH, host, realplugininstance, rrdfile)
                    info = rrdtool.info(str(rrdpath))
                    ds_list = set(k.split('[')[1].split(']')[0]
                                  for k in info
                                  if k.startswith('ds'))
                    for ds in ds_list:
                        all_ds_list.append(dict(rrdname=rrdname,
                                                dsname=ds))
                return render_to_response('browse.html',
                                          {'user' : request.user,
                                           'hosts' : hosts,
                                           'host': host,
                                           'plugininstance' : plugininstance,
                                           'plugininstances' : plugininstances,
                                           'ds_list': all_ds_list,
                                           })
        return render_to_response('browse.html', {'user' : request.user,
                                                'hosts' : hosts,
                                                'host' : host,
                                                'plugininstances' : plugininstances,
                                                })
    return render_to_response('browse.html',
                              {'user': request.user,
                               'hosts': hosts})


def dashboard(request):
    metrics = Dashboard.objects.filter(user=request.user.id)
    return render_to_response('dashboard.html', {'user' : request.user, 'metrics' : metrics})


def add_to_dashboard(request, host, plugininstance, rrdfile, datasource):
    obj, created = Dashboard.objects.get_or_create(user=request.user.id, host=host, plugininstance=plugininstance, rrdfile=rrdfile, datasource=datasource)
    return dashboard(request)


def remove_from_dashboard(request, host, plugininstance, rrdfile, datasource):
    Dashboard.objects.filter(user=request.user.id, host=host, plugininstance=plugininstance, rrdfile=rrdfile, datasource=datasource).delete()
    return dashboard(request)


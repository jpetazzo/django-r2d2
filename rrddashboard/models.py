from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    host = models.CharField(max_length=100)
    plugininstance = models.CharField(max_length=200)
    rrdfile = models.CharField(max_length=100)
    datasource = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        unique_together = [
            ['user', 'host', 'plugininstance', 'rrdfile', 'datasource']
        ]

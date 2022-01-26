from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User

class Construct(models.Model):
    """Construct.

    Attributes
    ----------

    """
    name = models.CharField(max_length=256, unique=True)
    des = models.CharField(max_length=256, unique=True)
    antigen = models.CharField(max_length=256, unique=True)
    vector = models.TextField(max_length=256, unique=True)
    project = models.CharField(max_length=256, unique=True)
    anti_res = models.CharField(max_length=256, unique=True)
    curator = models.CharField(max_length=256, unique=True)
    create-date = models.CharField(max_length=256, unique=True)
    made = models.CharField(max_length=256, unique=True)
    eln = models.CharField(max_length=256, unique=True)
    sequence = models.TextField()
    pf = models.CharField(max_length=256, unique=True)
    gisaid = models.CharField(max_length=256, unique=True)
    o_name = models.CharField(max_length=256, unique=True)
    promoter = models.CharField(max_length=256, unique=True)
    location = models.CharField(max_length=256, unique=True)
    note = models.CharField(max_length=256, unique=True)
    date = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

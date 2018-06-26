# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import warnings
warnings.filterwarnings("ignore")


class Applications(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(db_column='Additional_Info', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'applications'


class Catalogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    application = models.ForeignKey(Applications, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    max_decomposition_level = models.IntegerField(blank=True, null=True)
    min_channel_length = models.IntegerField(blank=True, null=True)
    classifier = models.CharField(max_length=100, blank=True, null=True)
    energy_type = models.CharField(max_length=30, blank=True, null=True)
    channels = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalogs'

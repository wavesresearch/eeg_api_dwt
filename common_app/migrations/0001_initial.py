# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-13 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('additional_info', models.TextField(blank=True, db_column='Additional_Info', null=True)),
            ],
            options={
                'db_table': 'applications',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Catalogs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('model', models.TextField(blank=True, null=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
                ('max_decomposition_level', models.IntegerField(blank=True, null=True)),
                ('min_channel_length', models.IntegerField(blank=True, null=True)),
                ('classifier', models.CharField(blank=True, max_length=100, null=True)),
                ('energy_type', models.CharField(blank=True, max_length=30, null=True)),
                ('channels', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'catalogs',
                'managed': False,
            },
        ),
    ]

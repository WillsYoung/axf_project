# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_for_homepage', '0005_auto_20180507_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainshow',
            name='brandname',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='categoryid',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='childcid1',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='childcid2',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='childcid3',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='productid1',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='productid2',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='mainshow',
            name='productid3',
            field=models.CharField(max_length=16, null=True),
        ),
    ]

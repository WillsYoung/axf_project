# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainMustBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_must_buy',
            },
        ),
        migrations.CreateModel(
            name='MainNavigate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_navigate',
            },
        ),
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('trackid', models.CharField(max_length=16)),
                ('img1', models.CharField(max_length=256)),
                ('longname1', models.CharField(max_length=128)),
                ('price1', models.FloatField(default=0)),
                ('marketprice1', models.FloatField(default=1)),
                ('img2', models.CharField(max_length=256)),
                ('longname2', models.CharField(max_length=128)),
                ('price2', models.FloatField(default=0)),
                ('marketprice2', models.FloatField(default=1)),
                ('img3', models.CharField(max_length=256)),
                ('longname3', models.CharField(max_length=128)),
                ('price3', models.FloatField(default=0)),
                ('marketprice3', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'axf_manshow',
            },
        ),
        migrations.CreateModel(
            name='MainWheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'axf_banner',
            },
        ),
    ]

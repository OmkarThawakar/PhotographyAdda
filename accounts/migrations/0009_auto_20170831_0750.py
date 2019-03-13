# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-31 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20170830_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='randomphoto',
            name='randomphoto_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

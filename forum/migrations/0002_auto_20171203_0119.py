# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-02 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='forum_photoes'),
        ),
    ]

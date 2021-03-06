# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-05 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(blank=True, upload_to='album_logo'),
        ),
    ]

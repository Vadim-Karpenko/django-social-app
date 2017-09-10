# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 14:59
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170819_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(default='users/default-photo.jpg', upload_to='users/%Y/%m/%d', verbose_name=''),
        ),
    ]

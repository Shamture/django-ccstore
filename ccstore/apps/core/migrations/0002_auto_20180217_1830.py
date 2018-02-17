# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-17 17:30
from __future__ import unicode_literals

import apps.core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_squashed_0002_auto_20180210_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(default=apps.core.models._default_currency, max_length=12, verbose_name='Currency'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-09 02:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]

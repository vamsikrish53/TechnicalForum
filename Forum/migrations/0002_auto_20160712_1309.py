# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-12 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_count',
            field=models.IntegerField(default=0),
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0002_auto_20170722_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailoption',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='detailoption',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='detailoption',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='productoption',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='productoption',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='productoption',
            name='parent',
        ),
    ]

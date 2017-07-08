# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20170708_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]

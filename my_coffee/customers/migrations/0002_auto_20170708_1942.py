# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedproduction',
            name='product',
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_productions',
            field=models.ManyToManyField(to='productions.Menu'),
        ),
        migrations.DeleteModel(
            name='OrderedProduction',
        ),
    ]

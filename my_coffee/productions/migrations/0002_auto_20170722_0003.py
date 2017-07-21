# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailoption',
            name='parent',
            field=models.ForeignKey(blank=True, to='productions.DetailOption', null=True),
        ),
        migrations.AddField(
            model_name='productoption',
            name='parent',
            field=models.ForeignKey(blank=True, to='productions.ProductOption', null=True),
        ),
    ]

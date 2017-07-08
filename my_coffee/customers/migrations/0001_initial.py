# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'W', max_length=1, choices=[(b'W', b'waiting'), (b'P', b'preparation'), (b'R', b'ready')])),
                ('price', models.IntegerField(default=0)),
                ('location', models.CharField(default=b'IS', max_length=2, choices=[(b'TA', b'take away'), (b'IS', b'in shop')])),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('product', models.ManyToManyField(to='productions.Menu')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_productions',
            field=models.ManyToManyField(to='customers.OrderedProduction'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]

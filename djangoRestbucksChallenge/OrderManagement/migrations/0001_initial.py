# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-23 18:03
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomizedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('preparation', 'preparation'), ('ready', 'ready'), ('delivered', 'delivered')], default='waiting', max_length=20)),
                ('location', models.CharField(choices=[('coffeeshop', 'coffeeshop'), ('takeaway', 'takeaway')], max_length=10)),
                ('order_time', models.DateTimeField(default=datetime.datetime.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customized_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderManagement.CustomizedProduct')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderManagement.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='customizedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrderManagement.Product'),
        ),
    ]

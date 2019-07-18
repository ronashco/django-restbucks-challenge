# Generated by Django 2.2.3 on 2019-07-18 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0003_auto_20190717_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('w', 'Waiting'), ('p', 'Preparation'), ('r', 'Ready'), ('d', 'Delivered')], default='w', max_length=1),
            preserve_default=False,
        ),
    ]

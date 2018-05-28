# Generated by Django 2.0.5 on 2018-05-28 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID_num', models.CharField(default='0', max_length=100)),
                ('production', models.CharField(max_length=100)),
                ('consume_location', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('waiting', 'waiting'), ('preparation', 'preperation'), ('ready', 'ready'), ('delivered', 'deliverd')], default='waiting', max_length=100)),
            ],
        ),
    ]

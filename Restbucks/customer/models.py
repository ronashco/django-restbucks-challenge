# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Order(models.Model):
    ID_number = 1
    ID_num = models.CharField(max_length=100, default='0')
    production = models.CharField(max_length=100)
    consume_location = models.CharField(max_length=100)

    STATE_CHOICES = (
        ('waiting', 'waiting'),
        ('preparation', 'preperation'),
        ('ready', 'ready'),
        ('delivered', 'deliverd'),
    )
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='waiting')

    def __str__(self):
        return self.production + ' : ' + self.consume_location
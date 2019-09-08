from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _


class Customer(AbstractUser):
    email = models.EmailField(verbose_name="email_address")
    AbstractUser._meta.get_field('username').verbose_name = "username"
    AbstractUser._meta.get_field('password').verbose_name = "password"

    def save(self, *args, **kwargs):
        return super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("customers")
        verbose_name = _("customer")

    def __str__(self):
        return self.username

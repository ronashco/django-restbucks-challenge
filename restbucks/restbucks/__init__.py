#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # NOQA

__all__ = ['celery_app']

DEFAULT_SETTINGS_MODULE = 'restbucks.settings.worker'

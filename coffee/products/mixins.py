from datetime import datetime
from django.db import models

class ModelTimeBaseMixin(models.Model):
    """Mixin for orders"""
    created_at = models.DateTimeField(default=datetime.utcnow, blank=True)
    updated_at = models.DateTimeField(default=datetime.utcnow, blank=True)

    class Meta:
        abstract = True

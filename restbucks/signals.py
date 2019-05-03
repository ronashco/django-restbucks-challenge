from django.db.models.signals import post_save
from django.dispatch import receiver

from restbucks.models import Order
from coffeeshop.common.utils import default_send_mail


@receiver(post_save, sender=Order)
def send_mail_for_change_order_status(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        default_send_mail(to=instance.user.email, status=instance.status)
    return


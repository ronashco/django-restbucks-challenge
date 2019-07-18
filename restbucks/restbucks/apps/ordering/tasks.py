from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _
from celery import shared_task


@shared_task
def send_status_email(user_email, status):
    send_mail(
        _(f'Your order status changed'),
        _('Hi\nYour request status changed to {status}'),
        settings.EMAIL_DEFAULT_SEND_ADDRESS,
        [user_email],
        fail_silently=True
    )

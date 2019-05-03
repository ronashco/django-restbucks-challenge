from django.core.mail import send_mail


def default_send_mail(to, status):
    # can do with celery task
    send_mail(
        subject='Order Status Changed',
        message='your order status change to %s' % status,
        from_email='admin@coffeeshop.com',
        recipient_list=[to],
        fail_silently=False,
    )

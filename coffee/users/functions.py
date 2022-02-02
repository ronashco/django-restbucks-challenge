"""In this file we create functions for user app"""
import os
import logging
from posix import environ
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_email_to_user(subject, template_body, recipient_email, template_context=None, **kwargs):
    """Email will be send to specific user with specified email"""
    mail = EmailMessage(subject=subject,
                        body=render_to_string(str(template_body), template_context),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[recipient_email])

    mail.fail_silently = False
    mail.content_subtype = 'html'
    mail.send()

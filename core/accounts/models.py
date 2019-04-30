from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(pre_save, sender=User)
def set_username(sender, instance=None, **kwargs):
    """
    For the sake of simplicity, We want to consider username as same as email,
    in every CREATE‌ operation with ORM, we set the username automatically.
    """
    instance.username = instance.email


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create a login token for every single user who created with ORM.
    """
    if created:
        Token.objects.create(user=instance)

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Login users with email instead the username.
    """
    def authenticate(self, *args, **kwargs):
        try:
            user = User.objects.get(email__iexact=kwargs['username'])
            if user and user.check_password(kwargs['password']):
                return user
            return None
        except User.DoesNotExist:
            return None

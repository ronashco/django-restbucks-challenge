from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class BaseTestCase(TestCase):
    @staticmethod
    def create_user(username, email, password, is_staff=False, is_superuser=False):
        user = UserModel(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()
        return user

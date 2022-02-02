import uuid
import logging
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from users.functions import send_email_to_user

logger = logging.getLogger('main')


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Default user creation funciton"""
        if not email:
            raise ValueError('Email must be set')
        try:
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.is_active = True # Set to True,
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Exception in user creation {e}")
            pass

    def create_superuser(self, email, password, **extra_fields):
        """Super user creation functionality"""
        try:
            user = self.create_user(email=email,
                                    password=password,
                                    is_admin=True,
                                    is_staff=True,
                                    is_active=True,
                                    is_superuser=True, **extra_fields)

            user.is_active = True
            user.save(using=self._db)

            return user
        except Exception as e:
            logger.error(f"Creating superuser was failed: {e}")


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(max_length=64, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name

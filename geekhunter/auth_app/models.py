from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class PortalUser(AbstractUser):
    is_staff = models.BooleanField(_('staff'), null=True)
    is_superuser = models.BooleanField(_('superuser'), null=True)
    phone = models.CharField(_('phone'), max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)

    REQUIRED_FIELDS = ['email', 'phone']

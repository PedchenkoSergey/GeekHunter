from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class PortalUser(AbstractUser):
    is_employee = models.BooleanField(_('employee'), default=False)
    is_company = models.BooleanField(_('company'), default=False)
    phone = models.CharField(_('phone'), max_length=50, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='user_photo', blank=True)

    REQUIRED_FIELDS = ['email', 'phone']

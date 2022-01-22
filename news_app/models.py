from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'draft'),
        ('APPROVED', 'approved'),

    ]
    title = models.CharField(_('title'), max_length=200, blank=False)
    text = models.CharField(_('text'), max_length=1000, blank=False)
    topik = models.CharField(_('topik'), max_length=100, blank=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

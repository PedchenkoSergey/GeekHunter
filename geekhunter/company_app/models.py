from django.db import models
from django.utils.translation import gettext_lazy as _

from auth_app.models import PortalUser
from employee_app.models import Resume


class Company(models.Model):
    name = models.CharField(_('name'), max_length=200, blank=False)
    specialization = models.CharField(_('specialization'), max_length=300, blank=True)
    short_description = models.CharField(_('short_description'), max_length=500, blank=True)

    def __str__(self):
        return self.name


class HrManager(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(PortalUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class FavoriteResume(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='fav_resumes')
    hr_manager = models.ForeignKey(HrManager, on_delete=models.CASCADE, related_name='hr_managers')

    def __str__(self):
        return f"{self.resume.__str__()} {self.hr_manager.__str__()}"


class Card(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'draft'),
        ('ACTIVE', 'active'),

    ]
    MODERATION_STATUSES = [
        ('UNDER_REVIEW', 'under_review'),
        ('APPROVED', 'approved'),
        ('NOT_APPROVED', 'not_approved'),
    ]
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(_('title'), max_length=200, blank=False)
    about = models.CharField(_('about'), max_length=500, blank=False)
    awards = models.CharField(_('awards'), max_length=500, blank=True)
    priorities = models.CharField(_('priorities'), max_length=500, blank=True)
    logo = models.ImageField(upload_to='company_logo', blank=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    moderation_status = models.CharField(
        _('moderation_status'), max_length=20,
        choices=MODERATION_STATUSES, default='UNDER_REVIEW',
    )
    error_text = models.CharField(_('error_text'), max_length=400, blank=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'draft'),
        ('ACTIVE', 'active'),

    ]
    MODERATION_STATUSES = [
        ('UNDER_REVIEW', 'under_review'),
        ('APPROVED', 'approved'),
        ('NOT_APPROVED', 'not_approved'),
    ]
    title = models.CharField(_('title'), max_length=200, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    description = models.CharField(_('description'), max_length=1000, blank=True)
    salary = models.CharField(_('salary'), max_length=400, blank=True)
    location = models.CharField(_('location'), max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    moderation_status = models.CharField(
        _('moderation_status'), max_length=20,
        choices=MODERATION_STATUSES, default='UNDER_REVIEW',
    )
    error_text = models.CharField(_('error_text'), max_length=400, blank=True)

    def __str__(self):
        return self.title


class Offer(models.Model):
    STATUS_CHOICES = [
        ('SENT', 'sent'),
        ('ACCEPTED', 'accepted'),
        ('NOT_ACCEPTED', 'not_accepted'),
    ]
    title = models.CharField(_('title'), max_length=200, blank=False)
    status = models.CharField(_('status'), choices=STATUS_CHOICES, max_length=20, default='SENT')
    text = models.CharField(_('text'), max_length=500, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, related_name='offers', null=True)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, related_name='offers', null=True)
    feedback = models.CharField(_('feedback'), max_length=500, blank=True)

    def __str__(self):
        return f"{self.title} {self.status}"

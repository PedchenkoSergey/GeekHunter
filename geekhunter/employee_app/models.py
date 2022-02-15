from django.db import models
from django.utils.translation import gettext_lazy as _

from auth_app.models import PortalUser


class Employee(models.Model):
    user = models.OneToOneField(PortalUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Resume(models.Model):
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
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    moderation_status = models.CharField(
        _('moderation_status'), max_length=20,
        choices=MODERATION_STATUSES, default='UNDER_REVIEW',
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='resumes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FavoriteVacancies(models.Model):
    vacancy = models.ForeignKey('company_app.Vacancy', on_delete=models.CASCADE, related_name='vacancies')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.vacancy.__str__()} {self.vacancy.company.__str__()}"


class Experience(models.Model):
    company = models.CharField(_('company'), max_length=200, blank=False)
    period = models.CharField(_('period'), max_length=200, blank=False)
    position = models.CharField(_('position'), max_length=300, blank=False)
    duties = models.CharField(_('duties'), max_length=1000, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience_resumes')

    def __str__(self):
        return self.position


class Education(models.Model):
    educational_institution = models.CharField(_('educational_institution'), max_length=400, blank=False)
    specialization = models.CharField(_('specialization'), max_length=300, blank=False)
    year_of_ending = models.CharField(max_length=5, null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education_resumes')

    def __str__(self):
        return self.educational_institution


class Courses(models.Model):
    company = models.CharField(_('company'), max_length=200, blank=False)
    specialization = models.CharField(_('specialization'), max_length=300, blank=False)
    year_of_ending = models.CharField(max_length=5, null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='courses_resumes')

    def __str__(self):
        return self.company


class Response(models.Model):
    STATUS_CHOICES = [
        ('SENT', 'sent'),
        ('ACCEPTED', 'accepted'),
        ('NOT_ACCEPTED', 'not_accepted'),
    ]
    title = models.CharField(_('title'), max_length=200, blank=False)
    status = models.CharField(_('status'), choices=STATUS_CHOICES, max_length=20, default='SENT')
    text = models.CharField(_('text'), max_length=500, blank=False)
    vacancy = models.ForeignKey('company_app.Vacancy', on_delete=models.SET_NULL, null=True, related_name='responses')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, related_name='responses')
    feedback = models.CharField(_('feedback'), max_length=500, blank=True)

    def __str__(self):
        return f"{self.title} {self.status}"

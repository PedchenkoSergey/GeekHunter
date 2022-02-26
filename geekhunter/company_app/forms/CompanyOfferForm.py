from django import forms

from employee_app.models import Resume
from ..models import Offer, Vacancy


class CompanyOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.resume_id = kwargs.pop('resume_id')
        super(CompanyOfferForm, self).__init__()
        self.fields['resume'].queryset = Resume.objects.filter(id=self.resume_id)
        self.fields['vacancy'].queryset = Vacancy.objects.filter(status='ACTIVE', moderation_status='APPROVED')

    class Meta:
        model = Offer
        fields = ('title', 'vacancy', 'resume', 'text')

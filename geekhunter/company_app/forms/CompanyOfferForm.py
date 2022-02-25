from django import forms

from employee_app.models import Resume
from ..models import Offer


class CompanyOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.resume_id = kwargs.pop('resume_id')
        super(CompanyOfferForm, self).__init__()
        self.fields['resume'].queryset = Resume.objects.filter(id=self.resume_id)

    class Meta:
        model = Offer
        fields = ('title', 'vacancy', 'resume', 'text')

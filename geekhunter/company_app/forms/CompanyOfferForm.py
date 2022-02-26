from django import forms

from company_app.models import Offer, Vacancy


class CompanyOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.resume_id = kwargs.pop('resume_id')
        self.request = kwargs.pop('request')
        super(CompanyOfferForm, self).__init__()
        self.fields['resume'].queryset = self.resume_id
        self.fields['resume'].initial = self.resume_id.first()
        self.fields['vacancy'].queryset = Vacancy.objects.filter(company_id=self.request.user.id, status='ACTIVE',
                                                                 moderation_status='APPROVED')

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['resume', 'vacancy']:
                field.widget.attrs['class'] = 'form-select'

    class Meta:
        model = Offer
        fields = ('title', 'vacancy', 'resume', 'text')

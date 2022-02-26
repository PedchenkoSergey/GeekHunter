from django import forms

from company_app.models import Offer


class EmployeeOfferAnswerForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('feedback',)

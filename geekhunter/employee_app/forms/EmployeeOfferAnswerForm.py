from django import forms

from company_app.models import Offer


class EmployeeOfferAnswerForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Offer
        fields = ('feedback',)

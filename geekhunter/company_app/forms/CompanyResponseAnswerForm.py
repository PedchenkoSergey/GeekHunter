from django import forms

from employee_app.models import Response


class CompanyResponseAnswerForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Response
        fields = ('feedback',)

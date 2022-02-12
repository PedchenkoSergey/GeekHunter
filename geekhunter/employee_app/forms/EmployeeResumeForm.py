from django import forms

from ..models import Resume


class EmployeeResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            'title', 'status'
        )

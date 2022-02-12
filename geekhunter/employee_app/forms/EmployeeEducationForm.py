from django import forms

from ..models import Education


class EmployeeEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['resume']

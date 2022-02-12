from django import forms

from ..models import Experience


class EmployeeExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['resume']

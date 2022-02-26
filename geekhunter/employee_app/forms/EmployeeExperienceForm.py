from django import forms
from django.forms import formset_factory

from employee_app.models import Experience


class EmployeeExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['resume']


ExperienceFormSet = formset_factory(EmployeeExperienceForm, extra=0)

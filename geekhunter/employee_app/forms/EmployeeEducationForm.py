from django import forms
from django.forms import formset_factory

from employee_app.models import Education


class EmployeeEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['resume']


EducationFormSet = formset_factory(EmployeeEducationForm, extra=0)

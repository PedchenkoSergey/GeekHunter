from django import forms

from ..models import Courses


class EmployeeCoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        exclude = ['resume']

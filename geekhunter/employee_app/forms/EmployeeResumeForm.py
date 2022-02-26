from django import forms

from employee_app.models import Resume


class EmployeeResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = (
            'title', 'status'
        )

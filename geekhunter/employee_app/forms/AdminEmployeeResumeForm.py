from django import forms

from employee_app.models import Resume


class AdminEmployeeResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'

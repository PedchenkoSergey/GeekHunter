from django import forms

from employee_app.models import Resume, Response


class EmployeeResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.vacancy_id = kwargs.pop('vacancy_id')
        self.request = kwargs.pop('request')
        super(EmployeeResponseForm, self).__init__()
        self.fields['vacancy'].queryset = self.vacancy_id
        self.fields['vacancy'].initial = self.vacancy_id.first()
        self.fields['resume'].queryset = Resume.objects.filter(employee_id=self.request.user.id, status='ACTIVE',
                                                               moderation_status='APPROVED')
        self.fields['resume'].initial = self.fields['resume'].queryset.first()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['resume', 'vacancy']:
                field.widget.attrs['class'] = 'form-select'

    class Meta:
        model = Response
        fields = ('title', 'vacancy', 'resume', 'text')

from django import forms

from company_app.models import Vacancy, HrManager, Company


class VacancyCreationForm(forms.ModelForm):
    STATUSES = [
        ('DRAFT', 'Черновик'),
        ('ACTIVE', 'Готов к публикации'),
    ]

    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название Должности'
    }))
    # company = forms.ModelChoiceField(queryset=Company.objects.get(id=product_id),widget=forms.Select(attrs={
    #     'placeholder': 'Название Компании'
    # }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Описание',
        'rows':'10',
        'style':"height:100%;"
    }))
    salary = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Зарплата'
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Место работы'
    }))

    status = forms.ChoiceField(widget=forms.Select(attrs={
        'placeholder': 'Черновик'
    }), choices=STATUSES)

    class Meta:
        model = Vacancy
        fields = (
            'title', 
            # 'company', 
            'description', 
            'salary', 
            'location', 
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'status':
                field.widget.attrs['id'] = 'floatingSelect'
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['id'] = 'floatingInput'
                
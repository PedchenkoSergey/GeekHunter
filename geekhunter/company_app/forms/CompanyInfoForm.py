from django import forms

from ..models import Company


class CompanyInfoForm(forms.ModelForm):
    logo = forms.ImageField(widget=forms.widgets.FileInput, required=False)

    class Meta:
        model = Company
        fields = ('name', 'specialization', 'short_description', 'logo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

from django import forms

from ..models import Card
from .widgets import BigTextarea


class AdminCompanyCardFrom(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {
            'about': BigTextarea,
            'priorities': BigTextarea,
            'awards': BigTextarea,
            'error_text': BigTextarea
        }
        fields = '__all__'

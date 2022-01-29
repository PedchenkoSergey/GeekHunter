from django import forms
from django.contrib.auth.forms import AuthenticationForm

from auth_app.models import PortalUser


class PortalUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'floatingInput',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'floatingPassword',
        'placeholder': 'Password'
    }))

    class Meta:
        model = PortalUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(PortalUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

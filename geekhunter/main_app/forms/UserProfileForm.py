from django import forms

from auth_app.models import PortalUser


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    avatar = forms.ImageField(widget=forms.widgets.FileInput, required=False)

    class Meta:
        model = PortalUser
        fields = ('username', 'password', 'first_name', 'last_name', 'phone', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'avatar':
                field.widget.attrs['type'] = 'file'
                field.widget.attrs['id'] = 'Avatar'

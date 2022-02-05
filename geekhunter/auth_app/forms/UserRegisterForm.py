from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.db import transaction

from auth_app.models import PortalUser
from company_app.models import HrManager, Company, Card
from employee_app.models import Employee


class PortalUserRegisterForm(UserCreationForm):
    ROLES = [
        ('EMPLOYEE', 'Employee'),
        ('COMPANY', 'Company')
    ]

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'name@example.com',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ivan'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ivanov'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your phone number'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))
    roles = forms.ChoiceField(widget=forms.Select(attrs={
        'placeholder': 'Role'
    }), choices=ROLES)

    class Meta:
        model = PortalUser
        fields = (
            'email', 'username', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'roles'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['password1', 'password2']:
                field.widget.attrs['id'] = 'floatingPassword'
            elif field_name == 'roles':
                field.widget.attrs['id'] = 'floatingSelect'
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['id'] = 'floatingInput'

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save()
        user.is_active = True
        role = self.cleaned_data['roles']

        if role == 'EMPLOYEE':
            user.is_employee = True
            permission = Permission.objects.get(codename='view_vacancy')
            user.user_permissions.add(permission)
            employee = Employee.objects.create(user=user)
        else:
            user.is_company = True
            company = HrManager.objects.create(
                user=user,
                company=Company.objects.create(
                    id=user.id,
                    name=f'компания {user.username}',
                    card=Card.objects.create(company_id=user.id)
                ),
            )

        user.save()
        return user

from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms.UserLoginForm import PortalUserLoginForm
from .forms.UserRegisterForm import PortalUserRegisterForm


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    title = 'Login'
    login_form = PortalUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user, user.is_active)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('main:index')
    context = {
        'title': title,
        'login_form': login_form
    }
    return render(request, 'auth_app/login_page.html', context)


def logout(request):
    auth.logout(request)
    return redirect('main:index')


def register(request):
    title = 'Sign Up'

    if request.method == 'POST':
        register_form = PortalUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            print(register_form.is_valid())
            register_form.save()
            return redirect('auth:login')

    else:
        register_form = PortalUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form,
    }

    return render(request, 'auth_app/sign_up_page.html', context)

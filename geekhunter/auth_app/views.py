from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms.UserLoginForm import PortalUserLoginForm
from .forms.UserRegisterForm import PortalUserRegisterForm


class PortalUserLoginView(LoginView):
    template_name = 'auth_app/login_page.html'
    form_class = PortalUserLoginForm
    redirect_authenticated_user = True
    extra_context = {
        'title': 'вход',
    }

    def get_success_url(self):
        return reverse_lazy('main_app:index')


class PortalUserLogoutView(LogoutView):
    next_page = 'main_app:index'


class PortalUserRegisterView(FormView):
    template_name = 'auth_app/sign_up_page.html'
    form_class = PortalUserRegisterForm
    extra_context = {
        'title': 'регистрация',
    }
    success_url = reverse_lazy('main_app:index')

    def form_valid(self, form):
        user = form.save()
        return super(PortalUserRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main_app:index')

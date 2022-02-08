from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import FormView
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from employee_app.models import FavoriteVacancies
from .forms.CompanyCardEditForm import CompanyCardEditForm
from .forms.VacancyCreationForm import VacancyCreationForm
from .models import Card, Vacancy, Company


class CompanyCardView(DetailView):
    template_name = 'company_app/company_card.html'
    queryset = Card.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().company.name
        context['card_data'] = serializers.serialize("python", [self.get_object()])
        return context


class VacanciesView(PermissionRequiredMixin, ListView):
    login_url = 'auth_app:login'
    permission_required = 'company_app.view_vacancy'
    template_name = 'company_app/vacancies.html'
    extra_context = {
        'title': 'вакансии',
        'favorite_vacancies': 'favorite_vacancies',

    }
    context_object_name = 'vacancies'
    ordering = ['-updated_at']

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Vacancy.objects.filter(
                company_id=self.kwargs.get('pk'),
                moderation_status='APPROVED',
                status='ACTIVE'
            ).order_by(*self.ordering)
        else:
            return Vacancy.objects.filter(moderation_status='APPROVED', status='ACTIVE').order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_vacancies'] = FavoriteVacancies.objects.filter(employee=self.request.user.id)
        return context


class VacancyCreationView(FormView):
    template_name = 'company_app/vacancy_create_page.html'
    form_class = VacancyCreationForm
    extra_context = {
        'title': 'Создание вакансии',
    }
    success_url = reverse_lazy('company_app:vacancies')

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.request.user.id)
        vacancy = Vacancy(
            title=request.POST.get('title'),
            company=company,
            description=request.POST.get('description'),
            salary=request.POST.get('salary'),
            location=request.POST.get('location'),
            status=request.POST.get('status')
        )
        vacancy.save()
        return HttpResponseRedirect(reverse('company_app:profile_vacancies'))


class CompanyProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile = Company.objects.get(id=request.user.id)
        return super(CompanyProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'title': f'профиль {self.profile.name}',
            'company': self.profile,
        }
        return render(request, 'company_app/company_profile.html', context)


class CompanyCardEditView(UpdateView):
    template_name = 'company_app/company_card_edit.html'
    queryset = Card.objects.all()
    model = Card
    form_class = CompanyCardEditForm
    success_url = reverse_lazy('company:profile')

    def get_form_kwargs(self):
        kwargs = super(CompanyCardEditView, self).get_form_kwargs()
        kwargs.update(instance={
            'card': self.object,
            'company': self.object.company,
        })
        return kwargs


class CompanyProfileVacanciesView(ListView):
    template_name = 'company_app/profille_vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(company_id=self.request.user.id)

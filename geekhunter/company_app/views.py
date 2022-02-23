from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import FormView
from django.core import serializers
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from employee_app.models import FavoriteVacancies
from .forms.CompanyCardEditForm import CompanyCardEditForm
from .forms.VacancyCreationForm import VacancyCreationForm
from .forms.VacancyEditForm import VacancyEditForm
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
    template_name = 'company_app/vacancy_create_or_update.html'
    form_class = VacancyCreationForm
    extra_context = {
        'title': 'Создание вакансии',
    }

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

    def get_context_data(self, **kwargs):
        context = super(CompanyCardEditView, self).get_context_data(**kwargs)
        context['company'] = self.get_object().company
        return context

    def get_form_kwargs(self):
        kwargs = super(CompanyCardEditView, self).get_form_kwargs()
        kwargs.update(instance={
            'card': self.object,
            'company': self.object.company,
        })
        print(kwargs['instance']['company'].logo)
        return kwargs

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(id=request.user.id)
        company.name = request.POST.get('company-name')
        company.short_description = request.POST.get('company-short_description')
        company.specialization = request.POST.get('company-specialization')

        card = Card.objects.get(company=company)
        card.title = request.POST.get('card-title')
        card.about = request.POST.get('card-about')
        card.awards = request.POST.get('card-awards')
        card.priorities = request.POST.get('card-priorities')
        card.status = request.POST.get('card-status')

        if request.FILES:
            logo = request.FILES['company-logo']
            logo_path = f'company_logo/company_{request.user.id}_logo.png'
            with default_storage.open(logo_path, 'wb+') as f:
                for chunk in logo.chunks():
                    f.write(chunk)
            company.logo = logo_path

        company.save()
        card.save()

        return HttpResponseRedirect(self.success_url)


class CompanyProfileVacanciesView(ListView):
    template_name = 'company_app/profille_vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(company_id=self.request.user.id)


class VacancyEditView(UpdateView):
    template_name = 'company_app/vacancy_create_or_update.html'
    queryset = Vacancy.objects.all()
    model = Vacancy
    form_class = VacancyEditForm
    success_url = reverse_lazy('company_app:profile_vacancies')


class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'company_app/vacancy_delete.html'
    context_object_name = 'vacancy'
    success_url = reverse_lazy('company:profile_vacancies')

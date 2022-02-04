from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from .forms.CompanyCardEditForm import CompanyCardEditForm
from .models import Card, Vacancy, Company


# Create your views here.

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
    extra_context = {'title': 'вакансии'}
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

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Card, Vacancy, Company


# Create your views here.

class CompanyCardView(DetailView):
    template_name = 'company_app/company_card.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Card, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['title'] = Company.objects.get(id=pk).name
        context['card_data'] = serializers.serialize("python", Card.objects.filter(company_id=pk))
        return context


class VacanciesView(PermissionRequiredMixin, ListView):
    login_url = 'auth_app:login'
    permission_required = 'company_app.view_vacancy'
    queryset = Vacancy.objects.filter(moderation_status='APPROVED', status='ACTIVE')
    template_name = 'company_app/vacancies.html'
    extra_context = {'title': 'вакансии'}
    context_object_name = 'vacancies'
    ordering = ['-updated_at']

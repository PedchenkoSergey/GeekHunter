from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Card, Vacancy


# Create your views here.

def get_company_card(request, pk=None):
    if pk is not None:
        if pk <= Card.objects.all().count():
            card = get_object_or_404(Card, pk=pk)
            card_data = serializers.serialize("python", Card.objects.filter(id=pk))
            context = {
                'title': 'company card',
                'card': card,
                'card_data': card_data,
            }
            if card.status == 'ACTIVE' and card.moderation_status == 'APPROVED':
                return render(request, 'company_app/company_card.html', context)
            else:
                return render(request, 'company_app/company_card_not_available.html', context)
        else:
            return redirect('main:index')


class VacanciesView(LoginRequiredMixin, ListView):
    login_url = 'auth_app:login'
    queryset = Vacancy.objects.filter(moderation_status='APPROVED', status='ACTIVE')
    template_name = 'company_app/vacancies.html'
    extra_context = {'title': 'вакансии'}
    context_object_name = 'vacancies'
    ordering = ['-updated_at']

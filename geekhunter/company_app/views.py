from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import FormView
from django.urls import reverse, reverse_lazy

from auth_app.models import PortalUser

from .models import Card, HrManager, Vacancy
from .forms.VacancyCreationForm import VacancyCreationForm


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
        hrmanager_company = HrManager.objects.get(user=PortalUser.objects.get(username=request.user)).company
        vacancy = Vacancy(
            title=request.POST.get('title'),
            company=hrmanager_company,
            description=request.POST.get('description'), 
            salary=request.POST.get('salary'),
            location=request.POST.get('location'),
            status=request.POST.get('status')
        )
        vacancy.save()
        return HttpResponseRedirect(reverse('company_app:vacancies'))

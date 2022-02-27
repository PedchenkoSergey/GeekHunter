from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import FormView
from django.core import serializers
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from company_app.forms.CompanyCardEditForm import CompanyCardEditForm
from company_app.forms.CompanyOfferForm import CompanyOfferForm
from company_app.forms.CompanyResponseAnswerForm import CompanyResponseAnswerForm
from company_app.forms.VacancyCreationForm import VacancyCreationForm
from company_app.forms.VacancyEditForm import VacancyEditForm
from company_app.models import Card, Vacancy, Company, Offer
from employee_app.models import FavoriteVacancies, Resume, Employee, Experience, Education, Courses, Response


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

    def post(self, request, *args, **kwargs):
        vacancy_id = request.POST.get('vacancy')
        vacancy = Vacancy.objects.get(id=vacancy_id)
        employee = Employee.objects.get(user_id=self.request.user.id)

        favorite_vacancy = FavoriteVacancies.objects.filter(
            vacancy=vacancy,
            employee=employee,
        )

        if not favorite_vacancy:
            favorite_vacancy = FavoriteVacancies.objects.create(
                vacancy=vacancy,
                employee=employee,
            )
            favorite_vacancy.save()

        return HttpResponseRedirect(reverse('company_app:vacancies'))


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


class MakeOfferView(FormView):
    form_class = CompanyOfferForm
    template_name = 'company_app/make_offer.html'
    success_url = reverse_lazy('employee:resumes')

    def get_form_kwargs(self):
        kwargs = super(MakeOfferView, self).get_form_kwargs()
        kwargs['resume_id'] = Resume.objects.filter(id=self.kwargs['resume_id'])
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super(MakeOfferView, self).get_initial()
        initial['resume'] = Resume.objects.get(id=self.kwargs['resume_id'])
        return initial

    def post(self, request, *args, **kwargs):
        offer = Offer(
            title=request.POST.get('title'),
            text=request.POST.get('text'),
            resume=Resume.objects.get(id=request.POST.get('resume')),
            vacancy=Vacancy.objects.get(id=request.POST.get('vacancy'))
        )
        offer.save()

        return HttpResponseRedirect(self.success_url)


class CompanyOffersListView(ListView):
    template_name = 'company_app/profile_offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.filter(vacancy__company=self.request.user.id)


class OfferDeleteView(DeleteView):
    model = Offer
    template_name = 'company_app/offer_delete.html'
    context_object_name = 'offer'
    success_url = reverse_lazy('company:profile_offers')


class CompanyResponsesView(ListView):
    template_name = 'company_app/profile_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(vacancy__company=self.request.user.id).filter(status__in=['SENT', 'ACCEPTED'])


class CompanyResponseAnswerView(FormView):
    template_name = 'company_app/response_answer.html'
    form_class = CompanyResponseAnswerForm
    success_url = reverse_lazy('company:profile_responses')

    def get_context_data(self, **kwargs):
        context = super(CompanyResponseAnswerView, self).get_context_data(**kwargs)
        context['response'] = Response.objects.get(id=self.kwargs['pk'])
        resume_id = context['response'].resume.id
        context['resume'] = Resume.objects.get(id=resume_id)
        context['experiencies'] = Experience.objects.filter(resume_id=resume_id)
        context['educations'] = Education.objects.filter(resume_id=resume_id)
        context['courses'] = Courses.objects.filter(resume_id=resume_id)
        return context

    def post(self, request, *args, **kwargs):
        response = self.get_context_data()['response']
        response.feedback = request.POST.get('feedback')
        if 'accept' in request.POST:
            response.status = 'ACCEPTED'
        else:
            response.status = 'NOT_ACCEPTED'
        response.save()

        return HttpResponseRedirect(self.success_url)

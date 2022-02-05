from django.urls import path

from .views import CompanyCardView, VacanciesView, VacancyCreationView

app_name = 'company_app'

urlpatterns = [
    path('<int:pk>/', CompanyCardView.as_view(), name='company_card'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/create/', VacancyCreationView.as_view(), name='vacancy_create'),

]

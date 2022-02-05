from django.urls import path

from .views import CompanyCardView, VacanciesView, CompanyProfileView, CompanyCardEditView, CompanyProfileVacanciesView, \
    VacancyCreationView

app_name = 'company_app'

urlpatterns = [
    path('<int:pk>/', CompanyCardView.as_view(), name='company_card'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacanciesView.as_view(), name='vacancies'),
    path('profile/vacancies/create/', VacancyCreationView.as_view(), name='vacancy_create'),
    path('profile/', CompanyProfileView.as_view(), name='profile'),
    path('profile/vacancies/', CompanyProfileVacanciesView.as_view(), name='profile_vacancies'),
    path('profile/card/edit/<int:pk>/', CompanyCardEditView.as_view(), name='card_edit'),
]

from django.urls import path

from .views import CompanyCardView, VacanciesView

app_name = 'company_app'

urlpatterns = [
    path('<int:pk>/', CompanyCardView.as_view(), name='company_card'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacanciesView.as_view(), name='vacancies'),
]

from django.urls import path

from .views import CompanyCardView, VacanciesView, CompanyProfileView, CompanyCardEditView

app_name = 'company_app'

urlpatterns = [
    path('<int:pk>/', CompanyCardView.as_view(), name='company_card'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacanciesView.as_view(), name='vacancies'),
    path('profile/', CompanyProfileView.as_view(), name='profile'),
    path('profile/card/edit/<int:pk>/', CompanyCardEditView.as_view(), name='card_edit'),
    # path('profile/card/create/<int:pk>/', CompanyCardCreateView.as_view(), name='card_create'),
]

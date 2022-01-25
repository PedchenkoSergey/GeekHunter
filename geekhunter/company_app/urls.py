from django.urls import path

from .views import get_company_card

app_name = 'company_app'

urlpatterns = [
    path('<int:pk>/', get_company_card, name='company_card'),
]

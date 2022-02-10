from django.urls import path
from .views import EmployeeProfileView

app_name = 'employee_app'

urlpatterns = [
    path('profile/', EmployeeProfileView.as_view(), name='profile'),
]
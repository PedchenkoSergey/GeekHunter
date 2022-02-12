from django.urls import path

from employee_app.views import ResumesView

app_name = 'employee_app'

urlpatterns = [
    path('resumes', ResumesView.as_view(), name='resumes'),
    path('resumes/<int:pk>/', ResumesView.as_view(), name='resumes'),
]

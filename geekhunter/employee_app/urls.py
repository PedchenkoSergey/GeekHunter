from django.urls import path

from .views import EmployeeProfileView, EmployeeProfileResumeView, ResumeCreationView, ResumeDetailView, \
    ResumeDeleteView

app_name = 'employee_app'

urlpatterns = [
    path('profile/', EmployeeProfileView.as_view(), name='profile'),
    path('profile/resumes/', EmployeeProfileResumeView.as_view(), name='profile_resumes'),

    path('profile/resumes/create/', ResumeCreationView.as_view(), name='resume_create'),
    path('profile/resumes/read/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),

    path('profile/resumes/delete/<int:pk>', ResumeDeleteView.as_view(), name='resume_delete'),
]

from django.urls import path


from .views import EmployeeProfileView, EmployeeProfileResumeView, ResumeCreationView, ResumeDetailView, \
    ResumeDeleteView, ResumeEditView, ResumesView, ResumeEntityDeleteView

app_name = 'employee_app'

urlpatterns = [
    path('profile/', EmployeeProfileView.as_view(), name='profile'),
    path('profile/resumes/', EmployeeProfileResumeView.as_view(), name='profile_resumes'),

    path('profile/resumes/create/', ResumeCreationView.as_view(), name='resume_create'),
    path('profile/resumes/read/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('profile/resumes/edit/<int:pk>/', ResumeEditView.as_view(), name='resume_edit'),
    path('profile/resumes/delete/<int:pk>/', ResumeDeleteView.as_view(), name='resume_delete'),

    path('profile/resume/entity_delete/', ResumeEntityDeleteView.as_view(), name='entity_delete'),

    path('resumes', ResumesView.as_view(), name='resumes'),
    path('resumes/<int:pk>/', ResumesView.as_view(), name='resumes'),
]

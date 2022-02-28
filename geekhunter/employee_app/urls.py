from django.urls import path


from employee_app.views import EmployeeProfileView, EmployeeProfileResumeView, ResumeCreationView, ResumeDetailView, \
    ResumeDeleteView, ResumeEditView, ResumesView, ResumeEntityDeleteView, EmployeeOffersView, EmployeeOfferAnswerView, \
    EmployeeResponsesListView, ResponseDeleteView, MakeResponseView

app_name = 'employee_app'

urlpatterns = [
    path('profile/', EmployeeProfileView.as_view(), name='profile'),
    path('profile/resumes/', EmployeeProfileResumeView.as_view(), name='profile_resumes'),

    path('profile/resumes/create/', ResumeCreationView.as_view(), name='resume_create'),
    path('profile/resumes/read/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('profile/resumes/edit/<int:pk>/', ResumeEditView.as_view(), name='resume_edit'),
    path('profile/resumes/delete/<int:pk>/', ResumeDeleteView.as_view(), name='resume_delete'),

    path('profile/resume/entity_delete/', ResumeEntityDeleteView.as_view(), name='entity_delete'),

    path('profile/offers/', EmployeeOffersView.as_view(), name='profile_offers'),
    path('profile/offers/answer/<int:pk>/', EmployeeOfferAnswerView.as_view(), name='offer_answer'),

    path('profile/responses/', EmployeeResponsesListView.as_view(), name='profile_responses'),
    path('profile/responses/delete/<int:pk>', ResponseDeleteView.as_view(), name='response_delete'),

    path('makeresponse/<int:vacancy_id>', MakeResponseView.as_view(), name='make_response'),

    path('resumes', ResumesView.as_view(), name='resumes'),
    path('resumes/<int:pk>/', ResumesView.as_view(), name='resumes'),
    path('resumes/view/<int:pk>/', ResumeDetailView.as_view(), name='resume_view'),
]
